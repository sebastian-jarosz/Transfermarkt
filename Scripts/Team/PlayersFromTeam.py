import requests
from bs4 import BeautifulSoup
import pandas as pd


def find_players_from_team(team_hyperlink):
    # For pretending being a browser
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # verein/teamid/season_id/year

    # Getting full page
    page_tree = requests.get(team_hyperlink, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

    table = page_soup.find("div", {"id": "yw1"})

    full_name_tags = table.find_all("span", {"class": "hide-for-small"})

    player_tags = []

    for fullNameTag in full_name_tags:
        player_tags.extend(fullNameTag.find_all("a", {"class": "spielprofil_tooltip"}))

    player_ids = []
    player_names = []
    player_hyperlinks = []

    for playerTag in player_tags:
        player_ids.append((playerTag['href'].rsplit('/', 1))[-1])
        player_names.append(playerTag.text)
        player_hyperlinks.append("https://www.transfermarkt.com" + playerTag['href'])

    return player_ids, player_names, player_hyperlinks
