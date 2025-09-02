
import os
from typing import Optional, Dict, Any

# Optional providers: OpenAI and Google Gemini. Fallback to stub if not configured.
def call_openai(prompt: str, model: str = None) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        import openai
        openai.api_key = api_key
        mdl = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        resp = openai.chat.completions.create(
            model=mdl,
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return None

def call_gemini(prompt: str, model: str = None) -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        mdl = model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        model = genai.GenerativeModel(mdl)
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return None

def stub_response(prompt: str) -> str:
    # Minimal deterministic response for offline demo
    return (
        "{\\n"
        "  \"query\": \"DEMO\",\\n"
        "  \"items\": [{\\n"
        "    \"context\": \"unity\",\\n"
        "    \"subtasks\": [{\\n"
        "      \"title\": \"Setup Teleport Locomotion\",\\n"
        "      \"steps\": [\\n"
        "        \"Install XR Interaction Toolkit\",\\n"
        "        \"Add XR Rig and Teleportation Provider\",\\n"
        "        \"Place Teleportation Areas and Anchors\",\\n"
        "        \"Bind input to teleport action\"\\n"
        "      ]\\n"
        "    }],\\n"
        "    \"code\": \"// C# sample code for teleport binding...\",\\n"
        "    \"gotchas\": [\"Enable continuous and snap turn separately\"],\\n"
        "    \"best_practices\": [\"Use action-based XR rig\"],\\n"
        "    \"difficulty\": \"medium\",\\n"
        "    \"docs_link\": \"https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit\"\\n"
        "  }],\\n"
        "  \"raw_sources\": []\\n"
        "}"
    )

def choose_and_call(provider: str, prompt: str) -> str:
    provider = (provider or "").lower()
    if provider == "openai":
        out = call_openai(prompt)
        if out: return out
    elif provider == "gemini":
        out = call_gemini(prompt)
        if out: return out
    else:
        # auto
        out = call_openai(prompt) or call_gemini(prompt)
        if out: return out
    # fallback
    return stub_response(prompt)
