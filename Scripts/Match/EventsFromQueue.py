import os
import time
from sys import platform
import PySimpleGUI as sg
import pandas as pd
from Scripts.Match.EventsFromMatch import get_events_from_match_pool, get_events_from_match
from Scripts.Match.MatchesFromQueue import get_matches_form_queue

if platform == "darwin":
    pass


def check_if_queue_file_exist(country_name, league_name, season, queue_number):
    if platform == "darwin":
        directory = os.environ['HOME'] + "/Desktop/Transfermarkt Export/" + country_name + "/" + str(
            season) + "/" + league_name + "/Matches"
        path = directory + "/" + str(queue_number) + ".xlsx"
    if platform == "win32":
        directory = os.environ['HOMEPATH'] + "\Desktop\Transfermarkt Export\\" + country_name + "\\" + str(
            season) + "\\" + league_name + "\Matches"
        path = directory + "\\" + str(queue_number) + ".xlsx"
    print(path)
    print(os.path.isfile(path))
    return os.path.isfile(path)


def generate_events_from_queue(country_name, league_name, season, queue_number, queue_hyperlink):
    print("Start of export for " + league_name + " " + str(season) + " " + str(queue_number))
    if platform == "darwin":
        directory = os.environ['HOME'] + "/Desktop/Transfermarkt Export/" + country_name + "/" + str(
            season) + "/" + league_name + "/Matches"
        path = directory + "/" + str(queue_number) + ".xlsx"
    if platform == "win32":
        directory = os.environ['HOMEPATH'] + "\Desktop\Transfermarkt Export\\" + country_name + "\\" + str(
            season) + "\\" + league_name + "\Matches"
        path = directory + "\\" + str(queue_number) + ".xlsx"
    matches_hyperlinks = get_matches_form_queue(queue_hyperlink)
    if not os.path.exists(directory):
        os.makedirs(directory)
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    temp_table1 = []
    temp_table2 = []
    temp_table3 = []
    temp_table4 = []

    if not matches_hyperlinks:
        raise BaseException

    for i in range(0, len(matches_hyperlinks)):
        print(matches_hyperlinks[i])
        time.sleep(1)
        temp_players_in_match_ids, temp_players_in_match_times, temp_goals_ids, temp_assists_ids = \
            get_events_from_match_pool(matches_hyperlinks[i], season)
        temp_table1.extend(temp_players_in_match_ids)
        temp_table2.extend(temp_players_in_match_times)
        temp_table3.append(temp_goals_ids)
        temp_table4.append(temp_assists_ids)

    df1 = pd.DataFrame(temp_table1)
    df1['TIMES'] = temp_table2
    df2 = pd.DataFrame(temp_table3)
    df3 = pd.DataFrame(temp_table4)
    df1.to_excel(writer, "PLAYERSINMATCH")
    df2.to_excel(writer, "GOALS")
    df3.to_excel(writer, "ASSISTS")
    writer.save()
    print("End of export for " + league_name + " " + str(season) + " " + str(queue_number))


def generate_events_from_queue_pool(country_name, league_name, season, queue_number, queue_hyperlink):
    sg.Popup("Start of export")
    print("Start of export for " + league_name + " " + str(season) + " " + str(queue_number))
    if platform == "darwin":
        directory = os.environ['HOME'] + "/Desktop/Transfermarkt Export/" + country_name + "/" + str(
            season) + "/" + league_name + "/Matches"
        path = directory + "/" + str(queue_number) + ".xlsx"
    if platform == "win32":
        directory = os.environ['HOMEPATH'] + "\Desktop\Transfermarkt Export\\" + country_name + "\\" + str(
            season) + "\\" + league_name + "\Matches"
        path = directory + "\\" + str(queue_number) + ".xlsx"
    matches_hyperlinks = get_matches_form_queue(queue_hyperlink)
    if not os.path.exists(directory):
        os.makedirs(directory)
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    temp_table1 = []
    temp_table2 = []
    temp_table3 = []
    temp_table4 = []

    for i in range(0, len(matches_hyperlinks)):
        sg.OneLineProgressMeter('Export', i, len(matches_hyperlinks), 'key', 'Export of events from queue')
        print(matches_hyperlinks[i])
        time.sleep(1)
        temp_players_in_match_ids, temp_players_in_match_times, temp_goals_ids, temp_assists_ids = get_events_from_match(
            matches_hyperlinks[i], season)
        temp_table1.extend(temp_players_in_match_ids)
        temp_table2.extend(temp_players_in_match_times)
        temp_table3.append(temp_goals_ids)
        temp_table4.append(temp_assists_ids)

    sg.OneLineProgressMeter('Export', len(matches_hyperlinks), len(matches_hyperlinks), 'key',
                            'Export of events from queue')
    df1 = pd.DataFrame(temp_table1)
    df1['TIMES'] = temp_table2
    df2 = pd.DataFrame(temp_table3)
    df3 = pd.DataFrame(temp_table4)
    df1.to_excel(writer, "PLAYERSINMATCH")
    df2.to_excel(writer, "GOALS")
    df3.to_excel(writer, "ASSISTS")
    writer.save()
    print("End of export for " + league_name + " " + str(season) + " " + str(queue_number))
    sg.Popup("End of export")
