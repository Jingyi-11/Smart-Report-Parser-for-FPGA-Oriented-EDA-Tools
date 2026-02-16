# cd ~/llm-parser
# source venv/bin/activate
# streamlit run Parser_UI.py

import streamlit as st
import os
from parse_all_report import batch_parse_rpt  
from llm_prompt_generator import build_prompt, query_llm  # GPT module

st.set_page_config(page_title="Vivado Report Analyzer", layout="centered")
st.title("📊 Vivado Report Analyzer with LLM")

# input path
report_path = st.text_input("📁 Enter report directory path", "/home/april-ai/Desktop/test_1/test_1.runs/impl_1/")

if st.button("🔍 Parse & Analyze"):
    if not os.path.isdir(report_path):
        st.error("❌ Invalid path. Please check the directory.")
    else:
        # parse report
        parsed = batch_parse_rpt(report_path)
        st.success("✅ Report parsed successfully!")

        # show extracted key info
        for file, content in parsed.items():
            st.subheader(f"📄 {file}")
            st.json(content)

        # generate Prompt and use LLM
        prompt = build_prompt(parsed)
        st.markdown("### 🤖 GPT Prompt Sent")
        st.code(prompt)

        with st.spinner("Asking LLM for suggestions..."):
            reply = query_llm(prompt)

        st.markdown("### ✅ LLM Suggestions")
        st.success(reply)
