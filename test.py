import requests
from bs4 import BeautifulSoup
import csv
import os

# Constants
URL = "http://di75wax.devweb.mwn.de"
OUTPUT_CSV = "products.csv"
LOG_CSV = "scraping_log.csv"
FOLDER = "./"

def fetchData():
    pass