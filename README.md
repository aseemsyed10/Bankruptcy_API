# Bankruptcy Prediction API — Historical Prototype

This is an early coursework version of my company bankruptcy prediction API, preserved to show development history. Current development is in [Bankruptcy_App_Final](https://github.com/aseemsyed10/Bankruptcy_App_Final), including [draft upgrade PR #1](https://github.com/aseemsyed10/Bankruptcy_App_Final/pull/1).

## What it demonstrates
- Logistic regression on company financial indicators
- FastAPI prediction endpoint (`POST /predict`)
- Early Streamlit frontend prototype

## Known limitations
- `main.py` loads a dataset from a machine-specific Windows location and retrains when imported. The referenced CSV is not included in this repository.
- The frontend requests `/validate`, which does not exist in the backend.
- The `/explain` endpoint calls an undefined `explainer`.
- The frontend hardcodes localhost, ignoring the Compose `API_URL`.
- Docker Compose references a frontend Dockerfile that is absent.
- The API accepts unnamed input features, so feature order must be managed externally.

This historical version is not a tested, deployable system and should not be used to make financial decisions.
