import datetime
import logging
import sys

from Scripts.League.CreateLeagueSaisonHyperlink import *
from Scripts.League.PlayersFromLeague import *
from Scripts.Match.EventsFromQueue import *
from Scripts.Other.CountriesFromTransfermarkt import get_countries_from_file

# logging info
logPath = os.path.realpath(__file__)

if platform == "darwin":
    logging.basicConfig(filename=logPath.rsplit('/', 1)[0] + '/app.log', filemode='w')
if platform == "win32":
    logging.basicConfig(filename=logPath.rsplit('\\', 1)[0] + '/app.log', filemode='w')
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# GUI VARIABLES

# Leagues
COUNTRIES = []
countriesJSON = get_countries_from_file()
for country in countriesJSON.keys():
    COUNTRIES.append(country)

LEAGUENAMES = []

# Get 10 years from this year
SEASONS = []
year = datetime.datetime.today().year
for quNumber in range(0, 10):
    tempSeason = str(year - quNumber) + '/' + str(year - quNumber + 1)
    SEASONS.append(tempSeason)

# Queues
QUEUES = []
for quNumber in range(1, 38):
    QUEUES.append(quNumber)

if platform == "darwin":
    image = os.environ['HOME'] + "/Desktop/GitHub/Transfermarkt/GUI/Logo.png"
if platform == "win32":
    image = os.environ['HOMEPATH'] + "\Desktop\MyProjects\Transfermarkt\GUI\Logo.png"

tab1_layout = [[sg.Text("Country"), sg.Combo(COUNTRIES, size=(100, 100), readonly="True", key='Country')],
               [sg.ReadButton('Change country')]]

tab2_layout = [[sg.Text("League"), sg.Combo(LEAGUENAMES, size=(100, 100), readonly="True", key='LeaguePlayers')],
               [sg.Text("Season"), sg.Combo(SEASONS, size=(100, 100), readonly="True", key='SeasonPlayers')],
               [sg.ReadButton('Export players')]]

tab3_layout = [[sg.Text("League"), sg.Combo(LEAGUENAMES, size=(100, 100), readonly="True", key="LeagueMatches")],
               [sg.Text("Season"), sg.Combo(SEASONS, size=(100, 100), readonly="True", key="SeasonMatches")],
               [sg.Text("Queue"), sg.Combo(QUEUES, size=(100, 100), readonly="True", key="QueueMatches")],
               [sg.ReadButton('Export matches from 1 to chosen queue'),
                sg.ReadButton('Export matches from chosen queue')]]

layout = [[sg.Image(image,
                    pad=(100, 0))],
          [sg.TabGroup([[sg.Tab('CHANGE COUNTRY FIRST', tab1_layout),
                         sg.Tab('Players from league', tab2_layout),
                         sg.Tab('Matches from queue', tab3_layout)]], pad=((100, 100), (100, 100)))],
          [sg.Exit()]]

window = sg.Window('S4S Transfermarkt Data Generator').Layout(layout)

while True:
    event, values = window.Read()

    if event is None or event == 'Exit':
        break

    elif event == 'Change country':
        LEAGUENAMES = []
        for league in countriesJSON[values['Country']]['leagues']:
            LEAGUENAMES.append(league['name'])
        window.FindElement('LeaguePlayers').Update(values=LEAGUENAMES)
        window.FindElement('LeagueMatches').Update(values=LEAGUENAMES)

    elif event == 'Export players':
        leagueHyperlink = None
        for league in countriesJSON[values['Country']]['leagues']:
            if league['name'] == values['LeaguePlayers']:
                leagueHyperlink = league['hyperlink']
        if leagueHyperlink is None:
            sg.PopupError(
                'Change country first. In ' + countriesJSON[values['Country']]['name'] + " there is no " + values[
                    'LeaguePlayers'])
            continue
        try:
            generate_list_of_players_from_league_pool(countriesJSON[values['Country']]['name'], values['LeaguePlayers'],
                                                      values['SeasonPlayers'].replace('/', '_'), leagueHyperlink)
        except:
            print('There is a problem with export of ' + countriesJSON[values['Country']]['name'] + " - " + values[
                'LeaguePlayers'])
            logging.error("Exception occurred", exc_info=True)
            sg.PopupError(
                'There is a problem with export of ' + countriesJSON[values['Country']]['name'] + " - " + values[
                    'LeaguePlayers'])

    elif event == 'Export matches from chosen queue':
        leagueHyperlink = None
        for league in countriesJSON[values['Country']]['leagues']:
            if league['name'] == values['LeagueMatches']:
                leagueHyperlink = league['hyperlink']
        if leagueHyperlink is None:
            sg.PopupError(
                'Change country first. In ' + countriesJSON[values['Country']]['name'] + " there is no " + values[
                    'LeaguePlayers'])
            continue
        try:
            generate_events_from_queue(countriesJSON[values['Country']]['name'], values['LeagueMatches'],
                                       values['SeasonMatches'].replace('/', '_'), values['QueueMatches'],
                                       generate_league_season_queue_hyperlink(leagueHyperlink,
                                                                              values['SeasonMatches'].split('/')[0],
                                                                              values['QueueMatches']))
        except Exception as e:
            print('There is a problem with export of ' + countriesJSON[values['Country']]['name'] + " - " + values[
                'LeaguePlayers'] + " - Queue: " + str(values['QueueMatches']))
            logging.error("Exception occurred", exc_info=True)
            sg.PopupError(
                'There is a problem with export of ' + countriesJSON[values['Country']]['name'] + " - " + values[
                    'LeaguePlayers'] + " - Queue: " + str(values['QueueMatches']) + ". Did You change countries?")
        except BaseException as e:
            sg.PopupError(
                'There is a problem with export of ' + countriesJSON[values['Country']]['name'] + " - " + values[
                    'LeaguePlayers'] + " - Queue: " + str(values['QueueMatches']) + ". No matches in that queue")
        sg.Popup('End of export')

    elif event == 'Export matches from 1 to chosen queue':
        leagueHyperlink = None
        for league in countriesJSON[values['Country']]['leagues']:
            if league['name'] == values['LeagueMatches']:
                leagueHyperlink = league['hyperlink']
        if leagueHyperlink is None:
            sg.PopupError(
                'Change country first. In ' + countriesJSON[values['Country']]['name'] + " there is no " + values[
                    'LeaguePlayers'])
            continue
        for quNumber in range(1, int(values['QueueMatches']) + 1):
            if check_if_queue_file_exist(countriesJSON[values['Country']]['name'], values['LeagueMatches'],
                                         values['SeasonMatches'].replace('/', '_'), quNumber) is not True:
                try:
                    generate_events_from_queue(countriesJSON[values['Country']]['name'], values['LeagueMatches'],
                                               values['SeasonMatches'].replace('/', '_'), quNumber,
                                               generate_league_season_queue_hyperlink(leagueHyperlink,
                                                                                      values['SeasonMatches'].split(
                                                                                          '/')[0], quNumber))
                except Exception as e:
                    print('There is a problem with export of ' + countriesJSON[values['Country']]['name'] + " - " +
                          values['LeaguePlayers'] + " - Queue: " + str(quNumber))
                    logging.error("Exception occurred", exc_info=True)
                    sg.PopupError(
                        'There is a problem with export of ' + countriesJSON[values['Country']]['name'] + " - " +
                        values['LeaguePlayers'] + " - Queue: " + str(quNumber) + ". Did You change countries?")
                except BaseException as e:
                    sg.PopupError(
                        'There is a problem with export of ' + countriesJSON[values['Country']]['name'] + " - " +
                        values['LeaguePlayers'] + " - Queue: " + str(quNumber) + ". No matches in that queue")
        sg.Popup('End of export')
