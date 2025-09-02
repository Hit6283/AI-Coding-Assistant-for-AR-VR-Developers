
from typing import Dict, Any
from .classifier import classify
from .search import web_search
from .prompts import build_prompt
from .providers import choose_and_call
from .schemas import CodeXROutput, OutputItem, Subtask

import json

def run_codexr(query: str, provider: str = "auto") -> CodeXROutput:
    context = classify(query)
    sources = web_search(query, k=4)
    prompt = build_prompt(query, context, sources)
    raw = choose_and_call(provider, prompt)

    # Ensure JSON
    try:
        data = json.loads(raw)
    except Exception as e:
        # Last-resort minimal valid object
        data = {
            "query": query,
            "items": [{
                "context": context,
                "subtasks": [{
                    "title": "Investigate task",
                    "steps": ["Identify environment", "Check docs", "Draft code"]
                }],
                "code": "// code placeholder",
                "gotchas": [],
                "best_practices": [],
                "difficulty": "medium",
                "docs_link": None
            }],
            "raw_sources": sources
        }
    # Validate & coerce
    return CodeXROutput(**data)
