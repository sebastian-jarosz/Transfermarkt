import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
from Scripts.Other.CountriesFromTransfermarkt import getCountriesFromTransfermarkt


print(getCountriesFromTransfermarkt())