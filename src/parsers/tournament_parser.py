"""
Tournament HTML parser for chess-results.com
"""

import re
from typing import List, Optional, Tuple
from bs4 import BeautifulSoup
from ..models.player import Player
from ..models.match import Match
from ..models.tournament import Tournament


class TournamentParser:
    """Parser for chess-results.com HTML pages"""

    @staticmethod
    def parse_player_info(soup: BeautifulSoup) -> Optional[Player]:
        """Extract player information from the page"""
        tables = soup.find_all("table", class_="CRs1")
        if not tables:
            return None

        name = "Unknown Player"
        starting_rank = None
        current_rank = None

        # First table contains player info
        table = tables[0]
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                label = cols[0].get_text(strip=True).lower()
                value = cols[1].get_text(strip=True)

                if label == "name":
                    name = value
                elif label == "starting rank":
                    starting_rank = value
                elif label == "rank":
                    current_rank = value

        return Player(
            name=name,
            snr="",  # SNR comes from config
            starting_rank=starting_rank,
            current_rank=current_rank,
        )

    @staticmethod
    def parse_total_rounds(soup: BeautifulSoup) -> int:
        """Extract total number of rounds from the page"""
        # Look for "Rd.X/Y" pattern in links
        for link in soup.find_all("a"):
            text = link.get_text(strip=True)
            match = re.search(r"Rd\.(\d+)/(\d+)", text)
            if match:
                return int(match.group(2))

        # Fallback: check pairing table
        tables = soup.find_all("table", class_="CRs1")
        if len(tables) >= 2:
            table = tables[1]
            rows = table.find_all("tr")
            max_round = 0
            for row in rows[1:]:
                cols = row.find_all("td")
                if len(cols) >= 1:
                    rd = cols[0].get_text(strip=True)
                    if rd.isdigit():
                        max_round = max(max_round, int(rd))
            return max_round

        return 0

    @staticmethod
    def find_result_column_index(headers) -> int:
        """Find the Result column index dynamically"""
        for i, h in enumerate(headers):
            header_text = h.get_text(strip=True).lower()
            if header_text == "res.":
                return i
        return 8  # Default fallback

    @staticmethod
    def parse_matches(soup: BeautifulSoup) -> List[Match]:
        """Extract all match results from the page"""
        tables = soup.find_all("table", class_="CRs1")
        if len(tables) < 2:
            return []

        # Second table contains matches
        table = tables[1]
        rows = table.find_all("tr")

        if not rows:
            return []

        # Find result column dynamically
        header_row = rows[0]
        headers = header_row.find_all("th")
        result_col_index = TournamentParser.find_result_column_index(headers)

        matches = []
        for row in rows[1:]:  # Skip header
            cols = row.find_all("td")
            if len(cols) >= 9:
                round_num = cols[0].get_text(strip=True)
                board_num = cols[1].get_text(strip=True)
                opponent_snr = cols[2].get_text(strip=True)
                opponent_name = cols[4].get_text(strip=True)
                result = (
                    cols[result_col_index].get_text(strip=True)
                    if len(cols) > result_col_index
                    else ""
                )

                match = Match(
                    round_number=round_num,
                    board_number=board_num,
                    opponent_snr=opponent_snr,
                    opponent_name=opponent_name,
                    result=result,
                    pairing="",  # Will be filled by color detection
                    color=None,
                )
                matches.append(match)

        return matches

    @staticmethod
    def parse_color_from_round_page(
        soup: BeautifulSoup, player_snr: str, opponent_snr: str
    ) -> Tuple[Optional[str], str]:
        """
        Parse round pairing page to determine player color
        Returns: (color, pairing_string)
        """
        tables = soup.find_all("table", class_="CRs1")
        if not tables:
            return None, f"{player_snr}-{opponent_snr}"

        table = tables[0]
        rows = table.find_all("tr")

        for row in rows[1:]:  # Skip header
            cols = row.find_all("td")
            if len(cols) >= 12:
                white_no = cols[1].get_text(strip=True)

                # Black number is usually in the last few columns
                black_no = ""
                for i in range(len(cols) - 1, max(10, len(cols) - 5), -1):
                    text = cols[i].get_text(strip=True)
                    if text.isdigit() and text != white_no:
                        black_no = text
                        break

                if white_no == player_snr:
                    return "White", f"{player_snr}-{opponent_snr}"
                elif black_no == player_snr:
                    return "Black", f"{opponent_snr}-{player_snr}"

        return None, f"{player_snr}-{opponent_snr}"

    @staticmethod
    def parse_tournament_state(
        soup: BeautifulSoup, tournament_id: str, player_snr: str
    ) -> Optional[Tournament]:
        """Parse complete tournament state from player page"""
        player = TournamentParser.parse_player_info(soup)
        if not player:
            return None

        player.snr = player_snr

        matches = TournamentParser.parse_matches(soup)
        total_rounds = TournamentParser.parse_total_rounds(soup)

        return Tournament(
            tournament_id=tournament_id,
            player=player,
            matches=matches,
            total_rounds=total_rounds,
        )
