"""
Player data model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    """Represents a chess player"""

    name: str
    snr: str  # Player serial number
    starting_rank: Optional[str] = None
    current_rank: Optional[str] = None
    federation: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.name} (SNR: {self.snr})"
