from voting import Session


def test_basic_tally():
    s = Session(name="Dinner")
    s.add_option("Pizza")
    s.add_option("Sushi")
    s.add_voter("Alice")
    s.add_voter("Bob")
    s.submit_scores("Alice", {"Pizza": 8, "Sushi": 5})
    s.submit_scores("Bob", {"Pizza": 6, "Sushi": 9})
    ranked = s.tally()
    assert ranked[0] == ("Pizza", 14)
    assert ranked[1] == ("Sushi", 14)


def test_clear_winner():
    s = Session(name="Weekend plan")
    s.add_option("Hiking")
    s.add_option("Movies")
    s.add_voter("Alice")
    s.add_voter("Bob")
    s.submit_scores("Alice", {"Hiking": 9, "Movies": 3})
    s.submit_scores("Bob", {"Hiking": 8, "Movies": 4})
    assert s.winner() == ["Hiking"]


def test_tie_detection():
    s = Session(name="Tie test")
    s.add_option("A")
    s.add_option("B")
    s.add_voter("Alice")
    s.submit_scores("Alice", {"A": 7, "B": 7})
    assert set(s.winner()) == {"A", "B"}


def test_score_clamping():
    s = Session(name="Clamp test")
    s.add_option("X")
    s.add_voter("Alice")
    s.submit_scores("Alice", {"X": 99})
    assert s.tally()[0][1] == 10


def test_voters_remaining():
    s = Session(name="Pending")
    s.add_voter("Alice")
    s.add_voter("Bob")
    s.add_option("X")
    s.submit_scores("Alice", {"X": 5})
    assert s.voters_remaining() == ["Bob"]
