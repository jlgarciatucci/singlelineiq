import json
import httpx
from app import config
from app.schemas import ValidationIssue

def explain_issues(issues: list[ValidationIssue], kpis: dict, nodes: list) -> list[dict]:
    """
    Orchestrates explaining validation issues. Selects between Mode A (Gemini)
    and Mode B (Fallback templates) based on config.
    """
    if config.USE_GEMINI and config.GOOGLE_API_KEY:
        try:
            return call_gemini_to_explain(issues, kpis, nodes)
        except Exception as e:
            print(f"Gemini reasoning failed: {e}. Falling back to templates.")
            return generate_fallback_explanations(issues)
    else:
        return generate_fallback_explanations(issues)

def call_gemini_to_explain(issues: list[ValidationIssue], kpis: dict, nodes: list) -> list[dict]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={config.GOOGLE_API_KEY}"
    
    simplified_issues = []
    for i in issues:
        simplified_issues.append({
            "issue_id": i.issue_id,
            "issue_type": i.issue_type,
            "title": i.title,
            "item_tag": i.item_tag,
            "parent_tag": i.parent_tag,
            "evidence": i.evidence
        })
        
    prompt = f"""
    You are an expert electrical design verification agent.
    You will receive a list of electrical design validation issues.
    For each issue, you must provide:
    1. explanation: A concise, plain-English engineering explanation of the issue.
    2. likely_impact: The likely impact of this issue on plant design or safety.
    3. recommended_action: A clear recommended action for the responsible engineer.
    4. confidence_note: A note about your confidence level based on the available evidence.

    CRITICAL RULES:
    - Do not create new issues.
    - Do not change any numerical values or names.
    - Do not invent equipment tags, parent-child relationships, or ratings.
    - If evidence is insufficient to explain an issue, state that evidence is insufficient.
    - Keep explanations concise, professional, and engineering-oriented.

    List of issues:
    {json.dumps(simplified_issues, indent=2)}

    Return a JSON array of objects with the keys:
    "issue_id", "explanation", "likely_impact", "recommended_action", "confidence_note".
    Only return the JSON array. Do not wrap in markdown block.
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "issue_id": {"type": "STRING"},
                        "explanation": {"type": "STRING"},
                        "likely_impact": {"type": "STRING"},
                        "recommended_action": {"type": "STRING"},
                        "confidence_note": {"type": "STRING"}
                    },
                    "required": ["issue_id", "explanation", "likely_impact", "recommended_action", "confidence_note"]
                }
            }
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    response = httpx.post(url, json=payload, headers=headers, timeout=60.0)
    response.raise_for_status()
    res_json = response.json()
    text = res_json["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)

def generate_fallback_explanations(issues: list[ValidationIssue]) -> list[dict]:
    out = []
    for i in issues:
        t = i.issue_type
        tag = i.item_tag or "Unknown"
        parent = i.parent_tag or "Unknown"
        ev = i.evidence or {}
        
        explanation = f"Issue of type {t} detected on item {tag}."
        likely_impact = "Risk to engineering deliverable integrity and model consistency."
        recommended_action = "Review spelling, data entry, and physical single-line diagrams."
        confidence_note = "Derived deterministically from the validation parser."
        
        if t == "ASSET_OVERLOAD":
            cap = ev.get("capacity_kw", "unknown")
            load = ev.get("downstream_load_kw", "unknown")
            util = ev.get("utilization_percent", "unknown")
            explanation = f"The downstream connected load of {load} kW exceeds the equipment capacity of {cap} kW (Utilization: {util}%)."
            likely_impact = "Risk of equipment overheating, protection tripping, and potential failure of the distribution board/mcc."
            recommended_action = "Verify capacity rating, redistribute downstream loads, or size up the equipment rating."
            confidence_note = "Calculated from consumer list ratings and hierarchical sum."
        elif t == "DUPLICATE_ITEM_TAG":
            count = ev.get("count", 2)
            explanation = f"The tag '{tag}' is defined {count} times in the consumer list."
            likely_impact = "Inconsistent load aggregation, potential mismatch in cabling calculations, and inventory confusion."
            recommended_action = "Rename the duplicate tag or consolidate the items if they represent the same physical asset."
            confidence_note = "Direct unique constraint check on item tags."
        elif t == "MISSING_RATED_POWER":
            explanation = f"The final load '{tag}' has a missing or null rated power column."
            likely_impact = "The downstream load of parent equipment will be underestimated in connected load studies."
            recommended_action = "Obtain vendor data sheet and input the rated power (kW)."
            confidence_note = "Identified via missing data check in consumer list parser."
        elif t == "PARENT_NOT_FOUND":
            miss = ev.get("missing_parent", parent)
            explanation = f"The parent tag '{miss}' specified for '{tag}' is missing from the consumer list."
            likely_impact = "Incomplete network graph, leading to under-reporting of total loading on transformers/mains."
            recommended_action = "Verify the correct parent tag spelling or add the missing parent equipment row."
            confidence_note = "Integrity constraint check on tree structure."
        elif t == "HIGH_VSD_CONCENTRATION":
            vsd_pct = ev.get("vsd_percent", 100.0)
            explanation = f"The share of VSD loads connected to '{tag}' is {vsd_pct}%, exceeding design criteria limits."
            likely_impact = "Increased harmonic distortion risk, possible resonance, and potential disruption to sensitive electronics."
            recommended_action = "Perform harmonic calculations and evaluate the need for active filters or line reactors."
            confidence_note = "Determined from motor starter types in consumer list."
        elif t == "VOLTAGE_MISMATCH":
            p_volt = ev.get("parent_voltage")
            c_volt = ev.get("child_voltage")
            if p_volt and c_volt:
                explanation = f"Voltage mismatch: parent is {p_volt} kV, child {tag} is {c_volt} kV."
            else:
                p_volt_sld = ev.get("parent_voltage_kv") or ev.get("consumer_voltage_kv")
                c_volt_sld = ev.get("child_voltage_kv") or ev.get("sld_voltage_kv")
                explanation = f"Voltage mismatch: parent voltage is {p_volt_sld} kV, child {tag} is {c_volt_sld} kV."
            likely_impact = "Incorrect equipment voltage rating specification or structural error in inferred tree."
            recommended_action = "Verify voltage specification sheets for both parent and child assets."
            confidence_note = "Derived from parent-child voltage comparison."
        elif t == "CONSUMER_ASSET_MISSING_FROM_SLD":
            explanation = f"The asset '{tag}' exists in the consumer list but is not visible in the CAD-exported SLD PDF."
            likely_impact = "Mismatched engineering deliverables, leading to construction site queries or incorrect documentation."
            recommended_action = "Update the single-line diagram PDF to include this asset or verify tag naming."
            confidence_note = "Cross-check between structured consumer CSV and visual extraction."
        elif t == "SLD_ONLY_ASSET":
            explanation = f"The asset '{tag}' is visible in the visual SLD but is missing from the consumer list database."
            likely_impact = "Purchasing and design lists may omit this equipment, causing procurement delays."
            recommended_action = "Insert the missing equipment row into the consumer list database."
            confidence_note = "Cross-check between visual extraction and structured consumer list."
        elif t == "PARENT_MISMATCH":
            c_parent = ev.get("consumer_parent")
            sld_parent = ev.get("sld_parent")
            explanation = f"The parent of '{tag}' in the consumer list is '{c_parent}', but the visual SLD shows parent '{sld_parent}'."
            likely_impact = "Inconsistent topological representations, possibly leading to incorrect cable sizing or routing."
            recommended_action = "Confirm the correct physical source of supply and update the matching document."
            confidence_note = "Comparison of parent tags across structured and visual graphs."
            
        out.append({
            "issue_id": i.issue_id,
            "explanation": explanation,
            "likely_impact": likely_impact,
            "recommended_action": recommended_action,
            "confidence_note": confidence_note
        })
    return out
