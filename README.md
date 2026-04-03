# Weighted Voting

A simple web app for making group decisions. Each person scores options from 1–10 and the highest total wins.

## Usage

1. Enter a session title (optional), the options to vote on, and the voters
2. Each voter scores every option from 1 (low) to 10 (high)
3. The app tallies the scores and shows the winner — ties are flagged explicitly

For voters, you can either enter names (one per line) or just a single number (e.g. `3`) to create 3 anonymous voters.

## Run locally

```bash
python3 -m venv voting_app_env
source voting_app_env/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`.

## Run tests

```bash
pytest tests/
# or a single test:
pytest tests/test_voting.py::test_tie_detection
```

## Deploy

Hosted on [Streamlit Community Cloud](https://share.streamlit.io) (free). To deploy:

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo
3. Set the main file to `app.py` and deploy

Any push to `main` triggers an automatic redeploy.
