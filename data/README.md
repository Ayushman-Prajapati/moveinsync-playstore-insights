# Data directory

- `reviews_seed.csv` contains five review examples transcribed or carefully paraphrased from public Google Play listing excerpts captured during the assignment research.
- Ratings are blank where the rating was not visible in the source excerpt. Do not infer or fill these values.
- This is an **illustrative seed sample**, not a representative sample of all reviews and not suitable for estimating category prevalence or average rating.
- Run `python -m pipeline.scrape_reviews --count 200` to attempt a fresh pull of publicly accessible reviews using `google-play-scraper`. Network access, Google Play availability, and rate limits may affect collection.
- If you add data, preserve the source URL and collection date, deduplicate by review ID/text, and respect applicable terms and rate limits.
