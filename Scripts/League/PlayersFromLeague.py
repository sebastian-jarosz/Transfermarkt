import os
import time
from multiprocessing import Pool
from sys import platform
import PySimpleGUI as sg
import pandas as pd
from Scripts.Player.AttributesFromPlayer import find_player_attributes
from Scripts.Team.PlayersFromTeam import find_players_from_team
from Scripts.Team.TeamsFromLeague import find_teams_from_league

if platform == "darwin":
    pass


def generate_list_of_players_from_league(country_name, league_name, season, league_hyperlink):
    sg.Popup("Start of export")
    team_ids, team_names, team_hyperlinks = find_teams_from_league(league_hyperlink)

    player_ids = []
    player_names = []
    player_teams = []
    player_hyperlinks = []
    player_positions = []
    player_feet = []
    player_agents = []
    player_dates_of_birth = []

    if platform == "darwin":
        directory = os.environ['HOME'] + "/Desktop/Transfermarkt Export/" + country_name + "/" + str(
            season) + "/" + league_name
        path = directory + "/Players.xlsx"
    if platform == "win32":
        directory = os.environ['HOMEPATH'] + "\Desktop\Transfermarkt Export\\" + country_name + "\\" + str(
            season) + "\\" + league_name
        path = directory + "\Players.xlsx"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(0, len(team_hyperlinks)):
        temp_ids, temp_names, temp_hyperlinks = find_players_from_team(team_hyperlinks[i])
        sg.OneLineProgressMeter('Export', i, len(team_hyperlinks), 'key', 'Export of players from teams')
        temp_team_name = team_names[i]
        print("Start of import for " + team_names[i])
        for j in range(0, (len(temp_ids))):
            player_teams.append(temp_team_name)
            time.sleep(1.5)
            temp_date_of_birth, temp_position, temp_agent, temp_foot = find_player_attributes(temp_hyperlinks[j])
            player_dates_of_birth.append(temp_date_of_birth)
            player_positions.append(temp_position)
            player_feet.append(temp_foot)
            player_agents.append(temp_agent)
        print("End of import for " + team_names[i])
        player_ids.extend(temp_ids)
        player_names.extend(temp_names)
        player_hyperlinks.extend(temp_hyperlinks)

    sg.OneLineProgressMeter('Export', len(team_hyperlinks), len(team_hyperlinks), 'key', 'Export of players from teams')
    df = pd.DataFrame({"ID": player_ids, "NAME": player_names, "TEAM": player_teams, "HYPERLINK": player_hyperlinks,
                       "DATE OF BIRTH": player_dates_of_birth, "POSITION": player_positions, "FOOT": player_feet,
                       "AGENT": player_agents})
    df.to_excel(path)

    sg.Popup("End of export")


def generate_list_of_players_from_league_pool(country_name, league_name, season, league_hyperlink):
    sg.Popup("Start of export")
    team_ids, team_names, team_hyperlinks = find_teams_from_league(league_hyperlink)

    player_ids = []
    player_names = []
    player_teams = []
    player_hyperlinks = []
    player_positions = []
    player_foots = []
    player_agents = []
    player_dates_of_birth = []

    if platform == "darwin":
        directory = os.environ['HOME'] + "/Desktop/Transfermarkt Export/" + country_name + "/" + str(
            season) + "/" + league_name
        path = directory + "/Players.xlsx"
    if platform == "win32":
        directory = os.environ['HOMEPATH'] + "\Desktop\Transfermarkt Export\\" + country_name + "\\" + str(
            season) + "\\" + league_name
        path = directory + "\Players.xlsx"
    if not os.path.exists(directory):
        os.makedirs(directory)

    p = Pool(50)
    records_teams_with_players = p.map(find_players_from_team, team_hyperlinks)
    p.terminate()
    p.join()

    for recordTeamWithPlayers in records_teams_with_players:
        temp_team_name = team_names[records_teams_with_players.index(
            recordTeamWithPlayers)]  # getting index of record in all records pooled before
        print("Start of import for " + temp_team_name)
        p = Pool(50)
        records_players_with_attributes = p.map(find_player_attributes, recordTeamWithPlayers[2])
        p.terminate()
        p.join()
        for record_player_with_attributes in records_players_with_attributes:
            player_teams.append(temp_team_name)
            player_dates_of_birth.append(record_player_with_attributes[0])
            player_positions.append(record_player_with_attributes[1])
            player_foots.append(record_player_with_attributes[3])
            player_agents.append(record_player_with_attributes[2])
        player_ids.extend(recordTeamWithPlayers[0])
        player_names.extend(recordTeamWithPlayers[1])
        player_hyperlinks.extend(recordTeamWithPlayers[2])
        print("End of import for " + temp_team_name)

    df = pd.DataFrame({"ID": player_ids, "NAME": player_names, "TEAM": player_teams, "HYPERLINK": player_hyperlinks,
                       "DATE OF BIRTH": player_dates_of_birth, "POSITION": player_positions, "FOOT": player_foots,
                       "AGENT": player_agents})
    df.to_excel(path)

    sg.Popup("End of export")
