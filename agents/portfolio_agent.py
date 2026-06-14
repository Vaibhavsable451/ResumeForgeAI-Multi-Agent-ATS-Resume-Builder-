import requests
from bs4 import BeautifulSoup


def get_portfolio_skills(
        url):

    try:

        html = requests.get(url, timeout=10).text

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        text = soup.get_text()

        return text[:5000]

    except (requests.RequestException, ValueError):
        return ""