import time
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup


def get_events_from_match(match_hyperlink, season):
    # For pretending being a browser
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = match_hyperlink
    match_id = match_hyperlink.rsplit('/', 1)[1]

    # Getting full page
    page_tree = requests.get(page, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

    starting_line_up_ids_tags = page_soup.findAll("span", {
        "class": ["aufstellung-rueckennummer-name", "spielprofil_tooltip", "tooltipstered"]})
    if len(starting_line_up_ids_tags) == 0:
        starting_line_up_tags = page_soup.find("h2", text="Line-Ups").parent.parent
        starting_line_up_ids_tags = starting_line_up_tags.findAll("a",
                                                                  {"class": ["spielprofil_tooltip", "tooltipstered"]})
    goal_table_tags = page_soup.find("div", {"id": "sb-tore"})
    substitutions_table_tags = page_soup.find("div", {"id": "sb-wechsel"})
    try:
        goal_players_tags = goal_table_tags.findAll("a", {"class": "wichtig"})
    except:
        goal_players_tags = []

    out_player_span_tags = substitutions_table_tags.findAll("span", {"class": "sb-aktion-wechsel-aus"})
    in_player_span_tags = substitutions_table_tags.findAll("span", {"class": "sb-aktion-wechsel-ein"})

    out_player_tags = []
    in_player_tags = []

    players_in_match_ids = []
    players_in_match_times = []
    starting_line_up_ids = []
    starting_line_ups_times = []
    goals_ids = []
    assists_ids = []
    in_ids = []
    in_times = []

    for id_tag in starting_line_up_ids_tags:
        time.sleep(1)
        player_link = "https://www.transfermarkt.com/a/leistungsdatendetails/spieler/" + id_tag[
            'id'] + "/plus/0?saison=" + season.split('_')[0] + "&verein=&liga=&wettbewerb=&pos=&trainer_id="
        player_page_tree = requests.get(player_link, headers=headers)
        player_page_soup = BeautifulSoup(player_page_tree.content, 'html.parser')
        minutes = player_page_soup.find("a", {"id": match_id}).findParent().findParent().find("td", {
            "class": "rechts"}).getText().split('\'')[0]
        starting_line_up_ids.append(id_tag['id'])
        starting_line_ups_times.append(minutes)

    for i in range(0, len(goal_players_tags)):
        # if even number
        if (i % 2 == 0):
            goals_ids.append((goal_players_tags[i])['id'])
        # if odd number
        else:
            assists_ids.append((goal_players_tags[i])['id'])

    for out_player_span_tag in out_player_span_tags:
        out_player_tags.extend(out_player_span_tag.findAll("a", {"class": "wichtig"}))

    for in_player_span_tag in in_player_span_tags:
        in_player_tags.extend(in_player_span_tag.findAll("a", {"class": "wichtig"}))

    for i in range(0, len(in_player_tags)):
        time.sleep(1)
        player_link = "https://www.transfermarkt.com/a/leistungsdatendetails/spieler/" + (in_player_tags[i])[
            'id'] + "/plus/0?saison=" + season.split('_')[0] + "&verein=&liga=&wettbewerb=&pos=&trainer_id="
        player_page_tree = requests.get(player_link, headers=headers)
        player_page_soup = BeautifulSoup(player_page_tree.content, 'html.parser')
        minutes = player_page_soup.find("a", {"id": match_id}).findParent().findParent().find("td", {
            "class": "rechts"}).getText().split('\'')[0]
        in_ids.append((in_player_tags[i])['id'])
        in_times.append(minutes)

    players_in_match_ids.extend(starting_line_up_ids)
    players_in_match_ids.extend(in_ids)
    players_in_match_times.extend(starting_line_ups_times)
    players_in_match_times.extend(in_times)

    return players_in_match_ids, players_in_match_times, goals_ids, assists_ids


def get_events_from_match_pool(match_hyperlink, season):
    # For pretending being a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = match_hyperlink
    match_id = match_hyperlink.rsplit('/', 1)[1]

    # Getting full page
    page_tree = requests.get(page, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

    starting_line_up_ids_tags = page_soup.findAll("span", {
        "class": ["aufstellung-rueckennummer-name", "spielprofil_tooltip", "tooltipstered"]})
    if len(starting_line_up_ids_tags) == 0:
        starting_line_up_tags = page_soup.find("h2", text="Line-Ups").parent.parent
        starting_line_up_ids_tags = starting_line_up_tags.findAll("a",
                                                                  {"class": ["spielprofil_tooltip", "tooltipstered"]})
    goal_table_tags = page_soup.find("div", {"id": "sb-tore"})
    substitutions_table_tags = page_soup.find("div", {"id": "sb-wechsel"})
    try:
        goal_players_tags = goal_table_tags.findAll("a", {"class": "wichtig"})
    except:
        goal_players_tags = []
    out_player_span_tags = substitutions_table_tags.findAll("span", {"class": "sb-aktion-wechsel-aus"})
    in_player_span_tags = substitutions_table_tags.findAll("span", {"class": "sb-aktion-wechsel-ein"})

    out_player_tags = []
    in_player_tags = []

    players_in_match_ids = []
    players_in_match_times = []
    starting_line_up_ids = []
    starting_line_ups_times = []
    goals_ids = []
    assists_ids = []
    in_ids = []
    in_times = []

    players_starting_hyperlinks = []

    for id_tag in starting_line_up_ids_tags:
        players_starting_hyperlinks.append(
            "https://www.transfermarkt.com/a/leistungsdatendetails/spieler/" + id_tag['id'] + "/plus/0?saison=" +
            season.split('_')[0] + "&verein=&liga=&wettbewerb=&pos=&trainer_id=" + match_id)
        starting_line_up_ids.append(id_tag['id'])

    p = Pool(50)
    starting_minutes = p.map(get_minutes_from_player, players_starting_hyperlinks)
    p.terminate()
    p.join()
    starting_line_ups_times.append(starting_minutes)

    for i in range(0, len(goal_players_tags)):
        # if even number
        if i % 2 == 0:
            goals_ids.append((goal_players_tags[i])['id'])
        # if odd number
        else:
            assists_ids.append((goal_players_tags[i])['id'])

    for out_player_span_tag in out_player_span_tags:
        out_player_tags.extend(out_player_span_tag.findAll("a", {"class": "wichtig"}))

    for in_player_span_tag in in_player_span_tags:
        in_player_tags.extend(in_player_span_tag.findAll("a", {"class": "wichtig"}))

    players_in_hyperlinks = []

    for i in range(0, len(in_player_tags)):
        players_in_hyperlinks.append(
            "https://www.transfermarkt.com/a/leistungsdatendetails/spieler/" + (in_player_tags[i])[
                'id'] + "/plus/0?saison=" + season.split('_')[
                0] + "&verein=&liga=&wettbewerb=&pos=&trainer_id=" + match_id)
        in_ids.append((in_player_tags[i])['id'])

    p = Pool(50)
    in_minutes = p.map(get_minutes_from_player, players_in_hyperlinks)
    p.terminate()
    p.join()
    in_times.append(in_minutes)

    players_in_match_ids.extend(starting_line_up_ids)
    players_in_match_ids.extend(in_ids)
    for time in starting_line_ups_times:
        players_in_match_times.extend(time)
    for time in in_times:
        players_in_match_times.extend(time)

    return players_in_match_ids, players_in_match_times, goals_ids, assists_ids


def get_minutes_from_player(playerHyperlink):
    link_prepared = playerHyperlink.rsplit('=', 1)[0] + '='
    match_id = playerHyperlink.rsplit('=', 1)[1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    player_page_tree = requests.get(link_prepared, headers=headers)
    player_page_soup = BeautifulSoup(player_page_tree.content, 'html.parser')
    minutes = \
        player_page_soup.find("a", {"id": match_id}).findParent().findParent().find("td",
            {"class": "rechts"}).getText().split('\'')[0]
    return minutes
