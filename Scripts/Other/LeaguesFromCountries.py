import requests
from bs4 import BeautifulSoup


def get_leagues_from_country(country_hyperlink):
    # For pretending being a browser
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # Getting full page
    page_tree = requests.get(country_hyperlink, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

    # Get main div
    h2 = page_soup.find('h2', text="Domestic leagues & cups")
    domestic_leagues_and_cups_div = h2.find_parent('div', {'class': "box"})
    a_tags = domestic_leagues_and_cups_div.findChildren('a')

    # tabs included in Domestic Leagues and Cups div
    not_used_tags = ["compact", "detailed"]
    hyperlink_beginning = "https://www.transfermarkt.com/jumplist/startseite/wettbewerb/"

    leagues = []
    for tag in a_tags:
        # empty string are false so here we will only get tags with proper text
        if tag.text.strip() and tag.text.lower() not in not_used_tags:
            league_id = tag['href'].split('/')[-1]
            league_hyperlink = hyperlink_beginning + league_id
            league = {'id': league_id, 'name': tag.text, 'hyperlink': league_hyperlink}
            if league['name'] not in ['ÖFB-Cup', 'Hrvatski nogometni kup', 'MOL Cup', 'Polish Cup', 'Superpuchar',
                                      'Slovnaft Cup', 'Kup Srbije', 'Ukrainian Cup', 'Ukrainian Super Cup']:
                leagues.append(league)

    print(leagues)
    return leagues
