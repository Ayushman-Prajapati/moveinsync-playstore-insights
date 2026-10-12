\
"""Analyze MoveInSync review CSVs. Keyword labels are heuristic, not ground truth."""
from pathlib import Path
import argparse
import pandas as pd
from pipeline.taxonomy import THEMES, OWNER_MAP, SEVERITY_MAP

DEFAULT_INPUT = Path("data/reviews_seed.csv")
DEFAULT_OUTPUT = Path("outputs")

def classify_text(text):
    text = str(text or "").lower()
    return [theme for theme, terms in THEMES.items() if any(term in text for term in terms)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path).fillna("")
    if "review_text" not in df.columns:
        raise SystemExit("Input CSV must contain a review_text column.")
    df["themes"] = df["review_text"].map(classify_text).map(lambda x: "|".join(x))
    df["primary_theme"] = df["themes"].map(lambda x: x.split("|")[0] if x else "unclassified")
    df["theme_count"] = df["themes"].map(lambda x: len(x.split("|")) if x else 0)
    df["primary_owner"] = df["primary_theme"].map(OWNER_MAP).fillna("Needs triage")
    df["suggested_severity_1_5"] = df["primary_theme"].map(SEVERITY_MAP).fillna(1)
    df.to_csv(output_dir / "classified_reviews.csv", index=False)

    exploded = df.assign(theme=df["themes"].str.split("|")).explode("theme")
    exploded = exploded[exploded["theme"].notna() & (exploded["theme"] != "")]
    if len(exploded):
        summary = (exploded.groupby("theme")
                   .agg(review_mentions=("review_id", "count"))
                   .reset_index()
                   .sort_values("review_mentions", ascending=False))
        summary["share_of_sample_reviews_pct"] = (summary["review_mentions"] / max(len(df), 1) * 100).round(1)
    else:
        summary = pd.DataFrame(columns=["theme", "review_mentions", "share_of_sample_reviews_pct"])
    summary.to_csv(output_dir / "theme_summary.csv", index=False)

    # Rating statistics use only rows with an explicitly available numeric rating.
    if "rating" in df.columns:
        numeric = pd.to_numeric(df["rating"], errors="coerce").dropna()
    else:
        numeric = pd.Series(dtype=float)
    rating_summary = {
        "input_file": str(input_path),
        "reviews_in_input": int(len(df)),
        "reviews_with_known_rating": int(len(numeric)),
        "mean_rating_known_only": round(float(numeric.mean()), 3) if len(numeric) else None,
        "one_or_two_star_count_known_only": int(numeric.isin([1, 2]).sum()) if len(numeric) else None,
        "warning": "Theme shares are shares of this input sample, not the Play Store population. Keyword labels require human validation."
    }
    pd.Series(rating_summary).to_json(output_dir / "run_summary.json", indent=2)
    print(f"Analyzed {len(df)} reviews. Outputs: {output_dir}")
    print("Known ratings:", len(numeric), "(unknown ratings are not imputed)")
    if len(summary):
        print(summary.to_string(index=False))
    print(rating_summary["warning"])

if __name__ == "__main__":
    main()
