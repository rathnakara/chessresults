"""
URL Parser for chess-results.com URLs
Extracts tournament ID, player SNR, and server from URLs
"""

import re
from urllib.parse import urlparse, parse_qs


def parse_chess_url(url):
    """
    Parse a chess-results.com URL to extract tournament ID, SNR, and server

    Example URLs:
    - https://s1.chess-results.com/tnr1280521.aspx?lan=1&art=9&fed=IND&snr=126&SNode=S0
    - https://s3.chess-results.com/tnr1264518.aspx?lan=1&art=9&fed=CHN&turdet=YES&flag=30&snr=1&SNode=S0

    Returns:
        dict: {'server': 's1', 'tournament_id': 'tnr1280521', 'player_snr': '126'}
        None if parsing fails
    """
    try:
        # Parse the URL
        parsed = urlparse(url)

        # Extract server (s1, s2, s3, etc.)
        hostname = parsed.hostname
        if hostname and "chess-results.com" in hostname:
            server_match = re.match(r"(s\d+)\.chess-results\.com", hostname)
            if server_match:
                server = server_match.group(1)
            else:
                server = "s1"  # Default to s1
        else:
            return None

        # Extract tournament ID from path
        path = parsed.path
        tournament_match = re.search(r"(tnr\d+)\.aspx", path)
        if not tournament_match:
            return None
        tournament_id = tournament_match.group(1)

        # Extract SNR from query parameters
        query_params = parse_qs(parsed.query)
        if "snr" not in query_params:
            return None
        player_snr = query_params["snr"][0]

        # Extract federation (fed) parameter, default to IND if not present
        federation = query_params.get("fed", ["IND"])[0]

        return {
            "server": server,
            "tournament_id": tournament_id,
            "player_snr": player_snr,
            "federation": federation,
        }

    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None
