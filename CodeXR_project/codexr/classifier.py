
from typing import Literal

def classify(query: str) -> Literal["unity", "unreal", "shader", "general"]:
    q = (query or "").lower()
    # Lightweight keyword rules
    unity_kw = ["unity", "c#", "monobehaviour", "xr toolkit", "teleport", "oculus", "openxr"]
    unreal_kw = ["unreal", "ue5", "blueprint", "c++", "multiplayer", "replication", "actor"]
    shader_kw = ["shader", "hlsl", "glsl", "shadergraph", "occlusion", "render", "fragment"]
    if any(k in q for k in unity_kw):
        return "unity"
    if any(k in q for k in unreal_kw):
        return "unreal"
    if any(k in q for k in shader_kw):
        return "shader"
    return "general"
