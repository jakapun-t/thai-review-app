import pandas as pd
import streamlit as st
from nlp_logic import analyze_text

st.set_page_config(page_title="Café Review Insights", page_icon="☕", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: #faf9f5;
        color: #3d3b37;
    }
    .block-container {
        max-width: 1000px;
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    h1, h2, h3, p, label, [data-testid="stMetricLabel"] {
        color: #3d3b37;
    }
    .hero {
        padding: 0.6rem 1.4rem;
        margin-bottom: 1rem;
        background: #edf2fb;
        border: 2px solid #494741;
        border-radius: 14px;
    }
    .hero h1 {
        margin: 0;
        font-size: 2.25rem;
        line-height: 1.25;
    }
    .hero p {
        margin: 0.2rem 0 0;
        color: #898579;
        font-size: 1.05rem;
    }
    .metric-card {
        min-height: 88px;
        padding: 0.8rem 1rem;
        border: 2px solid #494741;
        border-radius: 14px;
        background: #fff;
    }
    .metric-label {
        margin-bottom: 0.25rem;
        font-size: 1.05rem;
        font-weight: 600;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 750;
        line-height: 1;
    }
    [data-testid="stExpander"] {
        border: 2px dashed #57544d;
        border-radius: 12px;
    }
    [data-testid="stTabs"] button[role="tab"] {
        border: 2px solid #494741;
        border-radius: 10px;
        margin-right: 0.4rem;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        background: #3d3b37;
        color: #fff;
    }
    [data-testid="stDataFrame"], [data-testid="stArrowVegaLiteChart"] {
        border: 2px solid #494741;
        border-radius: 12px;
        overflow: hidden;
    }
    .footer {
        padding-top: 0.5rem;
        color: #989487;
        text-align: center;
    }
    </style>
    <div class="hero">
        <h1>☕ Café Review Insights</h1>
        <p>what customers talk about most</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Paste reviews (click to open)"):
    text = st.text_area(
        "Reviews",
        placeholder="Paste or type customer reviews here, one review per line...",
        height=150,
        label_visibility="collapsed",
    )
    top_n = st.slider("Number of words to show", min_value=1, max_value=20, value=5)

result = analyze_text(text, top_n=top_n)
top = pd.DataFrame(result["top_words"], columns=["word", "count"])

metric_columns = st.columns(3)
metrics = (
    ("📝 Reviews", result["lines"]),
    ("🔤 Words", result["word_count"]),
    ("✨ Unique words", result["unique_words"]),
)
for column, (label, value) in zip(metric_columns, metrics):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value:02d}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

chart_tab, table_tab = st.tabs(["Chart", "Table"])
with chart_tab:
    if top.empty:
        st.info("Paste a few reviews above to see the most-mentioned words.")
    else:
        st.bar_chart(top, x="word", y="count", horizontal=True, sort="-count")

with table_tab:
    if top.empty:
        st.info("Your top words will appear here after you add reviews.")
    else:
        st.dataframe(top, hide_index=True, use_container_width=True)

st.markdown('<div class="footer">made with Streamlit</div>', unsafe_allow_html=True)
