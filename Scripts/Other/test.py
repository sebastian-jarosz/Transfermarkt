import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
from CountriesFromTransfermarkt import getCountriesFromTransfermarkt


print(getCountriesFromTransfermarkt())