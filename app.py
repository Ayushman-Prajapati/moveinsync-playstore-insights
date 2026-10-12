\
"""Small Streamlit dashboard for the review-analysis outputs."""
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
from pipeline.analyze import classify_text

st.set_page_config(page_title="MoveInSync Play Store Insights", layout="wide")
st.title("MoveInSync Play Store Insights")
st.caption("Public review analysis prototype • theme labels are heuristic • validate before making decisions")

uploaded = st.file_uploader("Upload a review CSV (optional)", type=["csv"])
path = Path("data/reviews_seed.csv")
df = pd.read_csv(uploaded).fillna("") if uploaded else pd.read_csv(path).fillna("")
if "review_text" not in df:
    st.error("CSV needs a review_text column.")
    st.stop()

df["themes_list"] = df["review_text"].map(classify_text)
df["primary_theme"] = df["themes_list"].map(lambda xs: xs[0] if xs else "unclassified")
ratings = pd.to_numeric(df.get("rating", pd.Series(dtype=float)), errors="coerce").dropna()
c1, c2, c3 = st.columns(3)
c1.metric("Reviews in current sample", len(df))
c2.metric("Reviews with known rating", len(ratings))
c3.metric("Mean rating (known ratings)", f"{ratings.mean():.2f}/5" if len(ratings) else "Not available")

st.warning("The bundled five-review seed is illustrative, not representative. Do not infer overall issue prevalence or rating trends from it.")
st.subheader("Primary theme in current sample")
theme_counts = df["primary_theme"].value_counts().rename_axis("theme").reset_index(name="reviews")
st.plotly_chart(px.bar(theme_counts, x="theme", y="reviews", title="Primary theme (keyword heuristic)"), use_container_width=True)

st.subheader("Review explorer")
cols = [c for c in ["review_date", "rating", "reviewer", "primary_theme", "review_text", "source_url"] if c in df.columns]
st.dataframe(df[cols], use_container_width=True, hide_index=True)

st.subheader("Interpretation")
st.markdown("""
1. Validate automated labels against a manually coded sample.
2. Collect a larger, time-bounded sample before ranking issues.
3. Compare app versions and weeks only when dates/version metadata are available.
4. Pair review themes with product telemetry (booking success, GPS freshness, ETA error, notification latency, crashes).
""")
