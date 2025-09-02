
import os, json
import streamlit as st
from codexr import run_codexr
from codexr.schemas import CodeXROutput

st.set_page_config(page_title="CodeXR – AR/VR Coding Assistant", page_icon="🧠", layout="wide")

st.title("🧠 CodeXR — AI Coding Assistant for AR/VR (Unity • Unreal • Shader)")

st.markdown("""
Type a developer question. CodeXR returns subtasks, ready-to-paste code, gotchas, best practices, difficulty, and a docs link.
If no API keys are set, it will return a deterministic **offline demo** response.
""")

with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("Provider", ["auto", "openai", "gemini"], index=0)
    st.caption("Tip: set OPENAI_API_KEY or GEMINI_API_KEY in your environment for live responses.")
    st.divider()
    st.header("API Keys (optional)")
    st.text_input("OPENAI_API_KEY", type="password", key="openai_key")
    st.text_input("GEMINI_API_KEY / GOOGLE_API_KEY", type="password", key="gemini_key")
    st.text_input("SERPER_API_KEY (web search)", type="password", key="serper_key")
    st.text_input("BING_SEARCH_V7_KEY (web search)", type="password", key="bing_key")
    if st.button("Apply Keys to Session"):
        if st.session_state.openai_key: os.environ["OPENAI_API_KEY"] = st.session_state.openai_key
        if st.session_state.gemini_key: os.environ["GEMINI_API_KEY"] = st.session_state.gemini_key
        if st.session_state.serper_key: os.environ["SERPER_API_KEY"] = st.session_state.serper_key
        if st.session_state.bing_key: os.environ["BING_SEARCH_V7_KEY"] = st.session_state.bing_key
        st.success("Keys applied for current session.")

query = st.text_input("Ask CodeXR:", value="How do I add teleport locomotion in Unity VR?")

if st.button("Run CodeXR") or query:
    with st.spinner("Thinking..."):
        result: CodeXROutput = run_codexr(query, provider=provider)
    # Display
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("✅ Subtasks")
        for idx, item in enumerate(result.items, start=1):
            st.markdown(f"**Context:** `{item.context}` &nbsp;&nbsp; **Difficulty:** `{item.difficulty}`")
            for s in item.subtasks:
                st.markdown(f"- **{s.title}**")
                for step in s.steps:
                    st.markdown(f"  - {step}")
            st.divider()
        st.subheader("🧩 Code")
        st.code(result.items[0].code if result.items else "// no code", language="c" if result.items and result.items[0].context in ["unreal","shader"] else "python")
        st.subheader("⚠️ Gotchas")
        for g in (result.items[0].gotchas if result.items else []):
            st.markdown(f"- {g}")
        st.subheader("✅ Best Practices")
        for b in (result.items[0].best_practices if result.items else []):
            st.markdown(f"- {b}")
    with col2:
        st.subheader("📚 Docs Link")
        if result.items and result.items[0].docs_link:
            st.write(result.items[0].docs_link)
        else:
            st.write("—")
        st.subheader("🔗 Sources")
        for u in result.raw_sources:
            st.write(u)
        st.subheader("🧾 Raw JSON")
        st.code(json.dumps(result.dict(), indent=2))

st.caption("© CodeXR demo. For offline demo, leave API keys empty.")
