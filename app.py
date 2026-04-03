import streamlit as st
from voting import Session

st.set_page_config(page_title="Weighted Voting", page_icon="🗳️")
st.title("🗳️ Weighted Voting")

# ── Bootstrap session state ───────────────────────────────────────────────────
if "session" not in st.session_state:
    st.session_state.session = None
if "phase" not in st.session_state:
    st.session_state.phase = "setup"  # setup | voting | results


# ── Phase 1: Setup ────────────────────────────────────────────────────────────
if st.session_state.phase == "setup":
    st.subheader("Create a voting session")

    with st.form("setup_form"):
        session_name = st.text_input("Voting session title (optional)", placeholder="e.g. Friday dinner")

        options_raw = st.text_area(
            "Options (one per line)",
            placeholder="Pizza\nSushi\nTacos",
        )
        voters_raw = st.text_area(
            "Voters — one name per line, or just a number N for N anonymous voters",
            placeholder="Alice\nBob\nCarlos\n\nor just: 3",
        )
        submitted = st.form_submit_button("Start voting →")

    if submitted:
        options = [o.strip() for o in options_raw.splitlines() if o.strip()]
        stripped = voters_raw.strip()
        if stripped.isdigit():
            n = int(stripped)
            voters = [str(i) for i in range(1, n + 1)]
        else:
            voters = [v.strip() for v in voters_raw.splitlines() if v.strip()]

        if len(options) < 2:
            st.error("Add at least 2 options.")
        elif len(voters) < 1:
            st.error("Add at least 1 voter.")
        else:
            s = Session(name=session_name.strip())
            for o in options:
                s.add_option(o)
            for v in voters:
                s.add_voter(v)
            st.session_state.session = s
            st.session_state.phase = "voting"
            st.rerun()


# ── Phase 2: Voting ───────────────────────────────────────────────────────────
elif st.session_state.phase == "voting":
    s: Session = st.session_state.session
    remaining = s.voters_remaining()

    st.subheader(f"📋 {s.name}" if s.name else "📋 Voting in progress")
    st.caption(f"Voters remaining: {len(remaining)} of {len(s.voters)}")

    if not remaining:
        st.session_state.phase = "results"
        st.rerun()

    current_voter = remaining[0]
    voter_label = f"Voter {current_voter}" if current_voter.isdigit() else current_voter
    st.markdown(f"### {voter_label}'s turn")
    st.markdown("Score each option from **1** (low) to **10** (high).")

    with st.form(f"vote_form_{current_voter}"):
        scores = {}
        for option in s.options:
            scores[option] = st.slider(option, min_value=1, max_value=10, value=5)
        submitted = st.form_submit_button("Submit scores →")

    if submitted:
        s.submit_scores(current_voter, scores)
        st.rerun()


# ── Phase 3: Results ──────────────────────────────────────────────────────────
elif st.session_state.phase == "results":
    s: Session = st.session_state.session
    ranked = s.tally()
    winners = s.winner()

    st.subheader(f"🏆 Results — {s.name}" if s.name else "🏆 Results")

    if len(winners) > 1:
        st.warning(f"It's a tie between: **{', '.join(winners)}**")
    else:
        st.success(f"Winner: **{winners[0]}**")

    st.markdown("#### Full ranking")
    for rank, (option, total) in enumerate(ranked, start=1):
        max_possible = 10 * len(s.voters)
        st.progress(
            total / max_possible,
            text=f"{rank}. {option} — {total} pts",
        )

    with st.expander("Individual scores"):
        header = ["Voter"] + s.options
        rows = [
            [voter] + [s.scores.get(voter, {}).get(opt, "—") for opt in s.options]
            for voter in s.voters
        ]
        st.table([dict(zip(header, row)) for row in rows])

    if st.button("Start a new session"):
        st.session_state.session = None
        st.session_state.phase = "setup"
        st.rerun()
