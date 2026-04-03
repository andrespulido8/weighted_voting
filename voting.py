from dataclasses import dataclass, field


@dataclass
class Session:
    name: str
    options: list[str] = field(default_factory=list)
    voters: list[str] = field(default_factory=list)
    # scores[voter][option] = int score 1-10
    scores: dict[str, dict[str, int]] = field(default_factory=dict)

    def add_option(self, option: str) -> None:
        if option and option not in self.options:
            self.options.append(option)

    def add_voter(self, voter: str) -> None:
        if voter and voter not in self.voters:
            self.voters.append(voter)

    def submit_scores(self, voter: str, scores: dict[str, int]) -> None:
        """Record a voter's scores for all options. Scores are clamped to [1, 10]."""
        self.scores[voter] = {
            option: max(1, min(10, score)) for option, score in scores.items()
        }

    def voters_remaining(self) -> list[str]:
        """Return voters who have not yet submitted scores."""
        return [v for v in self.voters if v not in self.scores]

    def tally(self) -> list[tuple[str, int]]:
        """Return options ranked by total score, highest first."""
        totals = {
            option: sum(
                self.scores[voter].get(option, 0)
                for voter in self.voters
                if voter in self.scores
            )
            for option in self.options
        }
        return sorted(totals.items(), key=lambda x: x[1], reverse=True)

    def winner(self) -> list[str]:
        """Return the winning option(s). Multiple entries indicate a tie."""
        ranked = self.tally()
        if not ranked:
            return []
        top_score = ranked[0][1]
        return [option for option, score in ranked if score == top_score]
