"""
HTTP client for chess-results.com API
"""

import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from typing import Optional
from ..config import Config

# Suppress SSL warnings for chess-results.com
warnings.simplefilter("ignore", InsecureRequestWarning)


class ChessResultsClient:
    """HTTP client for fetching data from chess-results.com"""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.verify = config.verify_ssl

    def fetch_player_page(self) -> Optional[BeautifulSoup]:
        """Fetch and parse the player's tournament page"""
        url = self.config.get_player_url()
        return self._fetch_and_parse(url)

    def fetch_round_page(self, round_num: int) -> Optional[BeautifulSoup]:
        """Fetch and parse a specific round's pairing page"""
        url = self.config.get_round_url(round_num)
        return self._fetch_and_parse(url)

    def _fetch_and_parse(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch URL and return parsed BeautifulSoup object"""
        try:
            response = self.session.get(url, timeout=self.config.request_timeout)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            else:
                print(f"⚠️  Failed to fetch page: HTTP {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            print(f"⚠️  Request timeout after {self.config.request_timeout}s")
            return None
        except requests.exceptions.ConnectionError:
            print("⚠️  Connection error - check your internet connection")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
