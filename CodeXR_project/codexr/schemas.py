
from typing import List, Optional, Literal
from pydantic import BaseModel, HttpUrl, Field, validator

Difficulty = Literal["easy", "medium", "hard"]

class Subtask(BaseModel):
    title: str
    steps: List[str]

class OutputItem(BaseModel):
    context: Literal["unity", "unreal", "shader", "general"]
    subtasks: List[Subtask]
    code: str
    gotchas: List[str] = []
    best_practices: List[str] = []
    difficulty: Difficulty = "medium"
    docs_link: Optional[HttpUrl] = None

class CodeXROutput(BaseModel):
    query: str
    items: List[OutputItem]
    raw_sources: List[str] = Field(default_factory=list)

    @validator("items")
    def ensure_nonempty_items(cls, v):
        if not v:
            raise ValueError("items cannot be empty")
        return v
