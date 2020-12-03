import requests
from bs4 import BeautifulSoup


def get_leagues_from_country(country_hyperlink):
    # For pretending being a browser
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # verein/teamid/season_id/year

    # Getting full page
    page_tree = requests.get(country_hyperlink, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')
    leagues = []
    leagues_tags = page_soup.find('select', {'data-placeholder': 'Competition'}).findAll('option')
    del leagues_tags[0]  # delete empty record

    for leagueTag in leagues_tags:
        league = {'id': leagueTag['value'], 'name': leagueTag.text}
        league['hyperlink'] = 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/' + league['id']
        if league['name'] not in ['ÖFB-Cup', 'Hrvatski nogometni kup', 'MOL Cup', 'Polish Cup', 'Superpuchar',
                                  'Slovnaft Cup', 'Kup Srbije', 'Ukrainian Cup', 'Ukrainian Super Cup']:
            leagues.append(league)

    return leagues
