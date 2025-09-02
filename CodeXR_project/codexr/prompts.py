
SCHEMA_JSON = """
You must return ONLY valid JSON matching this schema:
{
  "query": "string",
  "items": [
    {
      "context": "unity|unreal|shader|general",
      "subtasks": [{"title":"string","steps":["string", "..."]}],
      "code": "string",
      "gotchas": ["string", "..."],
      "best_practices": ["string", "..."],
      "difficulty": "easy|medium|hard",
      "docs_link": "https://..."
    }
  ],
  "raw_sources": ["https://...", "..."]
}
"""

def build_prompt(query: str, context: str, sources: list[str]) -> str:
    src_block = "\\n".join(f"- {u}" for u in sources) if sources else "None"
    return f"""
You are CodeXR, an AI coding assistant for AR/VR developers.
User query: {query}
Detected context: {context}

Grounding sources (optional):
{src_block}

TASK:
- Break the task into clear subtasks with steps.
- Provide production-quality code for the detected context (Unity C#, Unreal C++, or HLSL/Shader).
- Include 3-6 gotchas and best practices.
- Rate difficulty.
- Include one authoritative documentation link from the sources if available (or a known official doc).
- Return ONLY valid JSON. No markdown fences, no prose.

{SCHEMA_JSON}
""".strip()
