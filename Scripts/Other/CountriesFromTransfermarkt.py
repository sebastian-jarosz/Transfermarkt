import codecs
import json
import os
from sys import platform
from bs4 import BeautifulSoup
from Scripts.Other.LeaguesFromCountries import get_leagues_from_country


def get_countries_from_transfermarkt():
    # 1580 line
    html_path = os.path.realpath(__file__)
    if platform == "darwin":
        html_path = html_path.rsplit('/', 1)[0] + "/transfermarkt.html"
    if platform == "win32":
        html_path = html_path.rsplit('\\', 1)[0] + "/transfermarkt.html"

    f = codecs.open(html_path, 'r', encoding='utf-8', errors=' ignore')

    countries = {}

    # Getting full page
    # pageTree = requests.get(f.read(), headers=headers)
    page_soup = BeautifulSoup(f, 'html.parser')

    countries_list = page_soup.find("select", {"data-placeholder": "Country"}).find_all('option')

    # When want more countries need to be added here
    needed_countries = ['Poland', 'Latvia', 'Lithuania', 'Serbia', 'Croatia', 'Czech Republic', 'Slovakia', 'Austria',
                        'Ukraine']

    del countries_list[0]  # delete empty record

    for country in countries_list:
        temp_country = {'id': country['value'], 'name': country.text}
        if temp_country['name'] in needed_countries:
            temp_country['hyperlink'] = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/' + country[
                'value']
            temp_country['leagues'] = get_leagues_from_country(temp_country['hyperlink'])
            countries[country.text] = temp_country

    with open(html_path.rsplit('/', 1)[0] + '/data.txt', 'w') as outfile:
        json.dump(countries, outfile)


def get_countries_from_file():
    htmlpath = os.path.realpath(__file__)

    if platform == "darwin":
        f = codecs.open(htmlpath.rsplit('/', 1)[0] + '/data.txt', 'r', encoding='utf-8', errors=' ignore')
    if platform == "win32":
        f = codecs.open(htmlpath.rsplit('\\', 1)[0] + '\data.txt', 'r', encoding='utf-8', errors=' ignore')
    countries = json.load(f)
    return countries
