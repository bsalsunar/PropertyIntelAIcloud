import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "backend"))

from ai_engine import analyze_listing_with_ai


st.set_page_config(
    page_title="PropertyIntelAI",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 PropertyIntelAI")
st.subheader("AI Property Listing Quality & SEO Analyzer")

st.write(
    "Paste a real estate listing below. The app compares it against a structured real estate knowledge base and uses AI to generate quality, SEO, and improvement recommendations."
)

listing_text = st.text_area(
    "Property Listing",
    height=220,
    placeholder="Example: Beautiful 3 bedroom home in Ames with updated kitchen and large backyard."
)

if st.button("Analyze Listing"):
    if not listing_text.strip():
        st.warning("Please enter a property listing.")
    else:
        with st.spinner("Analyzing listing..."):
            result = analyze_listing_with_ai(listing_text)

        st.success("Analysis completed.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Quality Score", result.get("quality_score", "N/A"))

        with col2:
            st.metric("SEO Score", result.get("seo_score", "N/A"))

        with col3:
            st.metric("Completeness Score", result.get("completeness_score", "N/A"))

        st.subheader("Missing Fields")
        for field in result.get("missing_fields", []):
            st.write(f"- {field}")

        st.subheader("AI Explanation")
        for item in result.get("explanation", []):
            st.write(f"- {item}")

        st.subheader("Recommended SEO Keywords")
        st.write(", ".join(result.get("seo_keywords", [])))

        st.subheader("Improvement Suggestions")
        for suggestion in result.get("improvement_suggestions", []):
            st.write(f"- {suggestion}")

        st.subheader("Improved SEO-Friendly Listing")
        st.write(result.get("improved_listing", "No improved listing generated."))
