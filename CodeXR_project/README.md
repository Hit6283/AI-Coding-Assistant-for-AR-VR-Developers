# CodeXR — AR/VR Coding Assistant (MVP)

A Streamlit demo that turns AR/VR developer questions into structured subtasks, code, gotchas, best practices, difficulty, and a docs link.

## Features
- Context classification (Unity / Unreal / Shader / General)
- Optional web search grounding (Serper.dev or Bing Web Search)
- LLM providers: OpenAI or Gemini; graceful offline stub when no keys present
- JSON schema validation via Pydantic
- Streamlit UI with raw JSON panel

## Quickstart
```bash
cd CodeXR
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
streamlit run app_streamlit.py
```

## Environment Variables (optional)
- `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`, default: gpt-4o-mini)
- `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) (and optionally `GEMINI_MODEL`, default: gemini-1.5-flash)
- `SERPER_API_KEY` for google.serper.dev
- `BING_SEARCH_V7_KEY` for Bing Web Search

If no keys are provided, the app responds with a deterministic offline demo JSON.

## Project Structure
```
CodeXR/
  app_streamlit.py
  codexr/
    __init__.py
    classifier.py
    pipeline.py
    prompts.py
    providers.py
    schemas.py
  pages/
    1_🎮_Unity_Demo.py
    2_🧱_Unreal_Demo.py
    3_🧪_Shader_Demo.py
  requirements.txt
  README.md
```

## Notes
- The offline stub ensures the UI is demo-able without networked LLMs.
- Replace the stub by setting API keys and re-running for real outputs.
```