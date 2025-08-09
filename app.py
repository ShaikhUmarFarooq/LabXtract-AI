import streamlit as st
import pandas as pd
from analyzer import load_tests, extract_pdf_text, analyze_text

st.set_page_config(page_title=" 🔬🩺 LabXtract AI-- Smart Medical Report Analyzer", layout="wide")

st.title("🔬🩺 LabXtract AI-- Smart Medical Report Analyzer")
st.markdown("Upload your **PDF medical report** and let AI analyze your test results with AI explanations.")

uploaded_pdf = st.file_uploader("📁 Upload Your PDF Report", type=["pdf"])
gender = st.selectbox("⚧️ Select Gender", ["Male", "Female"])

if uploaded_pdf and gender:
    with st.spinner("🔍 Analyzing your report using AI..."):
        try:
            all_tests = load_tests("normal_ranges.csv")
            text = extract_pdf_text(uploaded_pdf)
            result = analyze_text(text, all_tests, gender.lower())

            if result:
                st.success("✅ Analysis Complete!")
                df = pd.DataFrame(result)

                st.subheader("📘 Test Results")
                if "Explanation" in df.columns and df["Explanation"].str.strip().any():
                    st.dataframe(df[["Test Name", "Value", "Unit", "Normal Range", "Status", "Explanation"]], use_container_width=True)
                else:
                    st.dataframe(df[["Test Name", "Value", "Unit", "Normal Range", "Status"]], use_container_width=True)

                if all(r["Status"] == "Normal" for r in result):
                    st.success("🎉 Congratulations! All your test results are normal. Stay healthy and active! 🥦💪")

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Results as CSV", csv, file_name="report_analysis.csv", mime="text/csv")
            else:
                st.warning("⚠️ No recognizable test values found in the report.")

        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
