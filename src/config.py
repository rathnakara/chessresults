"""
Configuration module for chess tournament monitor
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Application configuration"""

    # API Settings
    check_interval: int = 30  # seconds between checks (increased from 5)
    request_timeout: int = 10  # seconds
    verify_ssl: bool = False  # chess-results.com has SSL issues

    # Display Settings
    show_progress_dots: bool = True
    use_emojis: bool = True

    # Tournament Settings
    server: str = "s1"
    tournament_id: str = ""
    player_snr: str = ""
    federation: str = "IND"

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables"""
        return cls(
            check_interval=int(os.getenv("CHECK_INTERVAL", 30)),
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", 10)),
            verify_ssl=os.getenv("VERIFY_SSL", "false").lower() == "true",
            show_progress_dots=os.getenv("SHOW_PROGRESS_DOTS", "true").lower()
            == "true",
            use_emojis=os.getenv("USE_EMOJIS", "true").lower() == "true",
        )

    def get_player_url(self) -> str:
        """Construct the player URL"""
        return (
            f"https://{self.server}.chess-results.com/{self.tournament_id}.aspx?"
            f"lan=1&art=9&fed={self.federation}&snr={self.player_snr}&SNode=S0"
        )

    def get_round_url(self, round_num: int) -> str:
        """Construct the round pairing URL"""
        return (
            f"https://{self.server}.chess-results.com/{self.tournament_id}.aspx?"
            f"lan=1&art=2&rd={round_num}&fed={self.federation}"
        )
