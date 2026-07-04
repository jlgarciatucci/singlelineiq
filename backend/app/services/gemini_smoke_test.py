from __future__ import annotations

import httpx

from app import config


def run_gemini_smoke_test() -> dict:
    if not config.USE_GEMINI:
        raise RuntimeError("USE_GEMINI is false.")
    if not config.GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.GEMINI_MODEL}:generateContent?key={config.GOOGLE_API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Return exactly this JSON object and nothing else: "
                            '{"status":"ok","source":"gemini_smoke_test"}'
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
        },
    }
    response = httpx.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30.0)
    response.raise_for_status()
    print(f"Gemini smoke test succeeded with model {config.GEMINI_MODEL}.")
    return {
        "ok": True,
        "model": config.GEMINI_MODEL,
        "status_code": response.status_code,
        "api_key_suffix": config.GOOGLE_API_KEY[-4:],
    }
