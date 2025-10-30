"""
Match/Game data model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Match:
    """Represents a single match/game in a tournament"""

    round_number: str
    board_number: str
    opponent_snr: str
    opponent_name: str
    result: str  # "1", "0", "0.5", or empty for TBD
    pairing: str  # e.g., "33-79" (white-black)
    color: Optional[str] = None  # "White", "Black", or None

    def is_completed(self) -> bool:
        """Check if the match has a result"""
        return bool(self.result.strip())

    def __str__(self) -> str:
        color_emoji = (
            "⚪" if self.color == "White" else "⚫" if self.color == "Black" else "⚫⚪"
        )
        result_str = self.result if self.result else "TBD"
        return (
            f"R{self.round_number} {color_emoji} vs {self.opponent_name}: {result_str}"
        )
