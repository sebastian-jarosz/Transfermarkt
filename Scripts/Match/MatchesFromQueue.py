import requests
from bs4 import BeautifulSoup


def get_matches_form_queue(queue_hyperlink):
    # For pretending being a browser
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = queue_hyperlink

    # Getting full page
    page_tree = requests.get(page, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

    all_matches_tags = page_soup.findAll("a", {"title": "Match Sheet"})

    match_hyperlinks = []

    for matchTag in all_matches_tags:
        match_hyperlinks.append("https://www.transfermarkt.com" + matchTag['href'])

    return match_hyperlinks
