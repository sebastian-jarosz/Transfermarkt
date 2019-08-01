from Scripts.League.PlayersFromLeague import generateListOfPlayersFromLeague
from Scripts.League.CreateLeagueSaisonHyperlink import *
import os

directory = os.environ['HOME'] + "/Desktop/Transfermark Export/"

if not os.path.exists(directory):
    os.makedirs(directory)

