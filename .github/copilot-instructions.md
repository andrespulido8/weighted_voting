# Copilot Instructions

## Project Overview

A weighted voting web app where a group of friends can score options (1–10) and the best option is selected by aggregated weighted score. Built with Python and Streamlit.

## Tech Stack

- **Language**: Python 3.11+
- **Web framework**: [Streamlit](https://docs.streamlit.io/) — UI is built entirely in Python, no HTML/CSS/JS
- **Dependency management**: `requirements.txt`
- **Deployment target**: Streamlit Community Cloud (reads directly from the GitHub repo)

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# The app opens at http://localhost:8501
```

## Project Structure (intended)

```
app.py               # Streamlit entry point — all UI lives here
voting.py            # Core voting logic (pure Python, no Streamlit imports)
requirements.txt     # Pinned dependencies
```

Keep business logic (`voting.py`) completely decoupled from Streamlit. This makes it independently testable.

## Core Domain Logic

- A **session** has a name, a list of **options**, and a list of **voters**
- Each voter assigns a score from **1 to 10** to each option
- The **weighted score** for an option = sum of all voters' scores for that option
- The option with the highest total score wins
- Ties should be surfaced explicitly (don't silently pick one)

## Key Conventions

- All voting/scoring logic goes in `voting.py` as plain functions or dataclasses — never import `streamlit` there
- Streamlit session state (`st.session_state`) is the persistence layer; there is no database
- Use `st.form` + `st.form_submit_button` for input flows to avoid re-runs on every keystroke
- Scores are integers in the range [1, 10]; validate and clamp on input

## Testing

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_voting.py

# Run a single test by name
pytest tests/test_voting.py::test_weighted_score_basic
```

Tests cover `voting.py` only — Streamlit UI is not unit tested.

## Deployment

The app is deployed via **Streamlit Community Cloud**:
1. Push to the `main` branch on GitHub
2. Streamlit Community Cloud auto-redeploys on every push
3. `requirements.txt` must be kept up to date — Community Cloud installs from it on each deploy
