import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd


#Get folder path
scriptpath = os.path.realpath(__file__)
scriptpath = scriptpath.rsplit('/', 1)[0]
print("Script path is : " + scriptpath)