import base64
import json
import httpx
from app import config

def extract_assets_from_pdf(pdf_path: str) -> list[dict]:
    """
    Sends the PDF file to Gemini API for visual asset extraction.
    Returns a list of dicts matching the SldAsset schema.
    """
    if not config.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not configured.")
        
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
        
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={config.GOOGLE_API_KEY}"
    
    prompt = """
    Analyze the attached electrical Single Line Diagram (SLD) PDF.
    Extract all visible electrical assets and their connections.
    For each asset, extract:
    - item_tag (e.g. KPL2-MAIN-3300-SWGR01, KPL2-A10-410-TR01)
    - asset_type (e.g. TA, HV, LV, MCC, UG, etc.)
    - parent_tag (the tag of the upstream feeding asset)
    - voltage_kv (numeric voltage in kV, if visible, e.g. 33.0, 6.6, 0.4)
    - capacity_kw (numeric rated power or capacity in kW, if visible, e.g. 6300.0, 1250.0)
    - confidence (a float from 0.0 to 1.0 representing your confidence in this extraction)
    - notes (any visible label or text near the asset)

    Return a JSON array of objects with the keys:
    "item_tag", "asset_type", "parent_tag", "voltage_kv", "capacity_kw", "confidence", "notes".
    Only return the JSON array, no Markdown wrapping or formatting.
    """
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": "application/pdf",
                            "data": pdf_base64
                        }
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "item_tag": {"type": "STRING"},
                        "asset_type": {"type": "STRING"},
                        "parent_tag": {"type": "STRING"},
                        "voltage_kv": {"type": "NUMBER"},
                        "capacity_kw": {"type": "NUMBER"},
                        "confidence": {"type": "NUMBER"},
                        "notes": {"type": "STRING"}
                    },
                    "required": ["item_tag"]
                }
            }
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    response = httpx.post(url, json=payload, headers=headers, timeout=60.0)
    response.raise_for_status()
    
    res_json = response.json()
    try:
        text = res_json["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to parse Gemini response: {e}. Raw response: {response.text}")
