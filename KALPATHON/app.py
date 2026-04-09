import re

import streamlit as st

from inference import generate_response
from model_loader import load_model


st.set_page_config(page_title="Legal Clause Simplifier", page_icon="⚖️", layout="centered")

st.markdown(
    """
    <style>
      .block-container { max-width: 880px; padding-top: 2.25rem; }
      .ls-card {
        border: 1px solid rgba(49, 51, 63, 0.15);
        border-radius: 14px;
        padding: 18px 18px 14px 18px;
        background: rgba(255,255,255,0.6);
      }
      .ls-output {
        border-radius: 14px;
        padding: 16px 16px 14px 16px;
        border: 1px solid rgba(49, 51, 63, 0.15);
        background: rgba(250, 250, 252, 0.95);
        white-space: pre-wrap;
        line-height: 1.55;
        font-size: 1.02rem;
      }
      .ls-risk {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.95rem;
        border: 1px solid rgba(49, 51, 63, 0.18);
      }
      .ls-risk-low { background: rgba(0, 170, 90, 0.14); color: rgb(0, 120, 65); }
      .ls-risk-medium { background: rgba(255, 193, 7, 0.18); color: rgb(140, 100, 0); }
      .ls-risk-high { background: rgba(220, 53, 69, 0.16); color: rgb(165, 30, 45); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Legal Clause Simplifier")
st.caption("AI-powered explanation of rental clauses")

# Pre-load model once and surface any errors early.
try:
    load_model()
except Exception as e:
    st.error("Model loading failed. Please check your `./model/` LoRA adapter folder and dependencies.")
    st.code(str(e))
    st.stop()

st.markdown('<div class="ls-card">', unsafe_allow_html=True)
clause = st.text_area(
    "Paste a rental agreement clause",
    height=220,
    placeholder="Example: The tenant shall be responsible for all repairs under $200, including normal wear and tear...",
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    run = st.button("Simplify Clause", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


def _split_risk_and_explanation(final_text: str) -> tuple[str, str]:
    t = (final_text or "").strip()
    m = re.match(r"^\s*(Low|Medium|High)\s+Risk\s*:\s*(.*)$", t, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return "Medium", t
    risk = m.group(1).capitalize()
    expl = (m.group(2) or "").strip()
    return risk, expl or t


if run:
    if not clause.strip():
        st.warning("Please enter a clause to simplify.")
    else:
        with st.spinner("Simplifying clause…"):
            try:
                final_text = generate_response(clause)
            except Exception as e:
                st.error("Inference failed. Please try again.")
                st.code(str(e))
                st.stop()

        risk, explanation = _split_risk_and_explanation(final_text)
        risk_class = {"Low": "ls-risk-low", "Medium": "ls-risk-medium", "High": "ls-risk-high"}.get(
            risk, "ls-risk-medium"
        )

        st.markdown(
            f'<span class="ls-risk {risk_class}">Risk Level: {risk}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="ls-output">{explanation}</div>',
            unsafe_allow_html=True,
        )