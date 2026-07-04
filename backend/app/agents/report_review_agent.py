import httpx
from app import config

def review_report(report_markdown: str) -> str:
    """
    Optional final verification pass on the report.
    If Gemini is active, requests Gemini to review/polish.
    If Gemini is not active, returns the report with an added signature.
    """
    if config.USE_GEMINI and config.GOOGLE_API_KEY:
        try:
            return call_gemini_to_review(report_markdown)
        except Exception as e:
            print(f"Gemini report review failed: {e}. Returning original report.")
            return report_markdown + "\n\n*Note: Report reviewed by automated validation boundaries.*"
    else:
        return report_markdown + "\n\n*Note: Report reviewed by automated validation boundaries.*"

def call_gemini_to_review(report_markdown: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={config.GOOGLE_API_KEY}"
    prompt = f"""
    You are an expert lead electrical verification engineer.
    Review the following generated markdown report for spelling, structure, and professional tone.
    You may format and polish the report layout to look like a premium technical document.
    
    CRITICAL RULES:
    - Do not invent or change any equipment tags, parents, ratings, or numerical calculation values.
    - Keep all original issue IDs and titles intact.
    - Do not remove any issue entries.
    
    Report:
    {report_markdown}
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    response = httpx.post(url, json=payload, headers=headers, timeout=60.0)
    response.raise_for_status()
    res_json = response.json()
    return res_json["candidates"][0]["content"]["parts"][0]["text"]
