# MoveInSync Play Store Insights

A repeatable, lightweight review-analysis project for the MoveInSync Forward Deployed Engineer candidate assignment.

**Goal:** turn public employee feedback into a prioritized, testable product-reliability plan, and make the analysis repeatable over time.

> **Important:** The bundled dataset contains five source-backed examples only. It is illustrative, not representative. The dashboard and scripts are a working prototype; the recommendations in the report are hypotheses to validate with a larger review sample and product telemetry.

## Initial research snapshot

- Google Play listing: 4.3 stars and approximately 114K reviews in the research snapshot (see [Sources](SOURCES.md)).
- The visible review excerpts identify potential issues with GPS/ETA reliability, booking dates/no-show disputes, check-in reminders, and booking-flow usability.
- A third-party tracker reported a recent 1,146-review sample with 4.10 average written-review rating and 25% one-star reviews. This is directional only; see `SOURCES.md` for limitations.

## Repository contents

```text
.
├── app.py                       Streamlit dashboard
├── data/
│   ├── README.md
│   └── reviews_seed.csv         Five illustrative public-review examples
├── pipeline/
│   ├── analyze.py               Theme classification and summary outputs
│   ├── scrape_reviews.py        Optional fresh public-review pull
│   └── taxonomy.py              Transparent theme taxonomy / ownership map
├── tests/test_analysis.py       Small unit-test suite
├── .github/workflows/tests.yml  CI checks
├── SOURCES.md                   URLs, snapshot and evidence limitations
├── requirements.txt
└── README.md
```

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pipeline.analyze
pytest -q
streamlit run app.py
```

Open the local Streamlit URL printed in the terminal.

## Pull a fresh sample

```powershell
python -m pipeline.scrape_reviews --count 200 --lang en --country in --output data/reviews_latest.csv
python -m pipeline.analyze --input data/reviews_latest.csv --output-dir outputs/latest
```

The pull may be limited by Google Play availability, network access, or rate limiting. Start with a modest count. The project does not bypass access controls. If a fresh pull fails, retain the seed data and retry later.

## How the analysis works

1. Load the review CSV.
2. Apply explainable keyword rules to assign one or more themes.
3. Export `classified_reviews.csv`, `theme_summary.csv`, and `run_summary.json`.
4. Explore the dataset in Streamlit.
5. Validate a sample of automated labels manually before using category percentages for prioritization.

The script does not infer missing star ratings. It only calculates rating statistics for rows with known numeric ratings.

## Proposed issue taxonomy

- Booking and scheduling
- GPS and ETA
- Notifications and check-in
- Login and stability
- Usability and UI
- Transport operations and safety
- Support and communication

These categories overlap. A review may be counted in more than one theme, so theme shares can sum to more than 100%.

## Prioritization model

The report recommends prioritizing by:
- Employee impact and safety/commute consequence
- Frequency in a sufficiently large, recent review sample
- Trend versus the previous period
- Product/engineering controllability
- Effort and confidence in the diagnosis

Do not rank issues by the seed dataset. It is too small and selected to illustrate known public complaints.

## Next steps for a production-ready version

- Collect a date-bounded sample of recent reviews and retain IDs, dates, ratings, app version and source URLs where available.
- Add manual labels for a validation set and measure classifier precision/recall.
- Add weekly snapshots and version-aware trend comparisons.
- Pair review themes with internal booking, GPS, notification, crash and support-ticket telemetry.
- Add alert thresholds only after a reliable baseline is established.

## Assignment note

Tools: Python, pandas, google-play-scraper, Streamlit, Plotly, pytest, GitHub Actions, and ChatGPT-assisted research synthesis. The source and limitations notes distinguish directly observed evidence from hypotheses and recommendations.
