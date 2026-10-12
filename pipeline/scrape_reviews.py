\
"""Pull a fresh sample of publicly accessible Google Play reviews."""
import argparse
from pathlib import Path
import pandas as pd

APP_ID = "com.moveinsync.ets"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=200)
    parser.add_argument("--output", default="data/reviews_latest.csv")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--country", default="in")
    args = parser.parse_args()
    try:
        from google_play_scraper import Sort, reviews
    except ImportError as exc:
        raise SystemExit("Install requirements first: pip install -r requirements.txt") from exc

    rows, token = [], None
    while len(rows) < args.count:
        batch, token = reviews(
            APP_ID, lang=args.lang, country=args.country, sort=Sort.NEWEST,
            count=min(100, args.count - len(rows)), continuation_token=token
        )
        if not batch:
            break
        rows.extend(batch)
        if token is None:
            break

    normalized = []
    for r in rows:
        normalized.append({
            "review_id": r.get("reviewId", ""),
            "review_date": r.get("at").date().isoformat() if r.get("at") else "",
            "reviewer": r.get("userName", ""),
            "rating": r.get("score", ""),
            "review_text": r.get("content", ""),
            "thumbs_up": r.get("thumbsUpCount", ""),
            "app_version": r.get("reviewCreatedVersion", "") or "",
            "source_url": f"https://play.google.com/store/apps/details?id={APP_ID}",
            "source_type": "google-play-scraper public review pull",
            "notes": "Pulled by pipeline.scrape_reviews"
        })
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(normalized).drop_duplicates(subset=["review_id", "review_text"]).to_csv(out, index=False)
    print(f"Saved {len(normalized)} reviews to {out}")
    if not normalized:
        print("No reviews returned. Keep the seed dataset and retry later; do not interpret an empty pull as zero reviews.")

if __name__ == "__main__":
    main()
