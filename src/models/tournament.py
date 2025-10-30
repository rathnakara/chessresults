"""
Tournament data model
"""

from dataclasses import dataclass, field
from typing import List, Optional
from .player import Player
from .match import Match


@dataclass
class Tournament:
    """Represents a chess tournament state"""

    tournament_id: str
    player: Player
    matches: List[Match] = field(default_factory=list)
    total_rounds: int = 0

    def get_completed_rounds(self) -> int:
        """Count how many rounds have been completed"""
        return sum(1 for match in self.matches if match.is_completed())

    def is_finished(self) -> bool:
        """Check if all rounds are completed"""
        return (
            self.total_rounds > 0 and self.get_completed_rounds() >= self.total_rounds
        )

    def get_latest_match(self) -> Optional[Match]:
        """Get the most recent match"""
        return self.matches[-1] if self.matches else None

    def __str__(self) -> str:
        completed = self.get_completed_rounds()
        return (
            f"Tournament {self.tournament_id}: {completed}/{self.total_rounds} rounds"
        )
