from Scripts.League.PlayersFromLeague import generateListOfPlayersFromLeague
from Scripts.League.CreateLeagueSaisonHyperlink import *

ekstraklasa = "https://www.transfermarkt.com/pko-ekstraklasa/startseite/wettbewerb/PL1"
# generateListOfPlayersFromLeague(ekstraklasa)

print(generateLeagueSaisonHyperlink(ekstraklasa, 2017))
print(generateLeagueSaisonQueueHyperlink(ekstraklasa, 2016, 30))