import requests
from bs4 import BeautifulSoup


def find_player_attributes(player_hyperlink):
    # For pretending being a browser
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = player_hyperlink

    print(player_hyperlink)

    # Getting full page
    page_tree = requests.get(page, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

    # Get birthdate and trim left and right white signs
    try:
        date_of_birth = page_soup.find("span", {"itemprop": "birthDate"}).text.strip().split('(')[0].strip()
    except:
        date_of_birth = "None"
    # Get span with text "Position:" then get next span with actual position of player, then stip spaces
    position = page_soup.find("span", text="Position:").findNext("span").text.strip()
    # Get span with text "Agent:" then get next span with actual agent of player,
    # then stip spaces (try in case there is an agent)
    try:
        agent = page_soup.find("span", text="Agent:").findNext("span").text.strip()
        if agent.endswith("..."):
            agent = page_soup.find("span", text="Agent:").findNext("a")["title"]
            if agent.startswith("<span"):
                agent = agent.split("\"")[3]
    except:
        agent = "None"
    try:
        foot = page_soup.find("th", text="Foot:").findNext("td").getText()
    except:
        foot = "No information"
    return date_of_birth, position, agent, foot
