"""
Tournament monitoring service
"""

import time
from typing import Optional, Dict, Tuple
from ..config import Config
from ..api.client import ChessResultsClient
from ..parsers.tournament_parser import TournamentParser
from ..models.tournament import Tournament
from ..models.match import Match


class TournamentMonitor:
    """Monitors a chess tournament and detects changes"""

    def __init__(self, config: Config, client: ChessResultsClient):
        self.config = config
        self.client = client
        self.parser = TournamentParser()
        self.pairing_cache: Dict[str, Tuple[Optional[str], str]] = {}
        self.last_tournament_state: Optional[Tournament] = None
        self.last_round_count: int = 0

    def fetch_current_state(self) -> Optional[Tournament]:
        """Fetch the current tournament state"""
        soup = self.client.fetch_player_page()
        if not soup:
            return None

        tournament = self.parser.parse_tournament_state(
            soup, self.config.tournament_id, self.config.player_snr
        )

        if not tournament:
            return None

        # Enrich matches with color information
        for match in tournament.matches:
            if match.opponent_snr and match.round_number:
                color, pairing = self._get_color_and_pairing(
                    match.round_number, match.opponent_snr
                )
                match.color = color
                match.pairing = pairing

        return tournament

    def _get_color_and_pairing(
        self, round_num: str, opponent_snr: str
    ) -> Tuple[Optional[str], str]:
        """Get color and pairing string for a match (with caching)"""
        # Check cache first
        if round_num in self.pairing_cache:
            return self.pairing_cache[round_num]

        # Fetch from API
        print(f"⏳ Fetching pairing info for Round {round_num}...", flush=True)
        soup = self.client.fetch_round_page(int(round_num))

        if soup:
            color, pairing = self.parser.parse_color_from_round_page(
                soup, self.config.player_snr, opponent_snr
            )
        else:
            color = None
            pairing = f"{self.config.player_snr}-{opponent_snr}"

        # Cache the result
        self.pairing_cache[round_num] = (color, pairing)
        return color, pairing

    def detect_new_round(self, tournament: Tournament) -> Optional[Match]:
        """Detect if a new round has been paired"""
        current_round_count = len(tournament.matches)

        # New round detected if count increased and it's not the first fetch
        if current_round_count > self.last_round_count and self.last_round_count > 0:
            return tournament.get_latest_match()

        return None

    def has_state_changed(self, tournament: Tournament) -> bool:
        """Check if tournament state has changed since last check"""
        if self.last_tournament_state is None:
            return True

        # Compare match results
        if len(tournament.matches) != len(self.last_tournament_state.matches):
            return True

        for new_match, old_match in zip(
            tournament.matches, self.last_tournament_state.matches
        ):
            if new_match.result != old_match.result:
                return True

        # Compare ranks
        if (
            tournament.player.current_rank
            != self.last_tournament_state.player.current_rank
        ):
            return True

        return False

    def update_state(self, tournament: Tournament):
        """Update the stored tournament state"""
        self.last_tournament_state = tournament
        self.last_round_count = len(tournament.matches)

    def run(self, callback=None):
        """
        Main monitoring loop

        Args:
            callback: Optional function called on each update with (tournament, new_round)
        """
        print("⏳ Starting monitor... (Press Ctrl+C to stop)\n")

        consecutive_failures = 0
        max_failures = 5

        try:
            while True:
                try:
                    tournament = self.fetch_current_state()

                    if not tournament:
                        consecutive_failures += 1
                        print(
                            f"\n⚠️  Failed to fetch tournament data (attempt {consecutive_failures}/{max_failures})"
                        )

                        # Send error via callback if too many failures
                        if consecutive_failures >= max_failures:
                            error_msg = f"Failed to fetch tournament data after {max_failures} attempts. Check network connection or tournament URL."
                            print(f"❌ {error_msg}")
                            if callback:
                                # Send error as a special update
                                callback(None, None, error=error_msg)
                            # Reset counter and continue trying
                            consecutive_failures = 0

                        time.sleep(self.config.check_interval)
                        continue

                    # Reset failure counter on success
                    consecutive_failures = 0

                    # Check if state has changed
                    if self.has_state_changed(tournament):
                        new_round = self.detect_new_round(tournament)

                        if callback:
                            callback(tournament, new_round)

                        self.update_state(tournament)

                        # Check if tournament is finished
                        if tournament.is_finished():
                            print("\n" + "🏁 " * 30)
                            print("✅ ALL ROUNDS COMPLETED! Tournament finished.")
                            print("🏁 " * 30)
                            break
                    else:
                        # Show progress indicator
                        if self.config.show_progress_dots:
                            print(".", end="", flush=True)

                except Exception as e:
                    print(f"\n❌ Error during monitoring: {e}")

                time.sleep(self.config.check_interval)

        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user.")

        print("\n✅ Program ended.")
