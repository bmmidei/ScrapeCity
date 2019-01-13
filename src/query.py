from bs4 import BeautifulSoup as BS
from src.parse import parse_availTable
import requests


def get_buildings(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BS(page.content, 'html.parser')

    # Examine the placard containers. Each placard represents an apartment
    # building.
    headers = soup.find_all('header', {'class': 'placardHeader'})
    buildings = {}
    for header in headers:
        url = header.find('a', {'class': 'placardTitle'}).get('href')
        name = header.find('a', {'class': 'placardTitle'}).get('title')
        buildings[name] = url

    # Return a dictionary of names and urls to each building's listings
    return buildings

def get_apartments(url):
    # For a given apartment building, extract the listing information for
    # the available units
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BS(page.content, 'html.parser')

    # Examine the availability table
    table = soup.find("table", {"class": "availabilityTable"})
    apt_info = parse_availTable(table)
    '''
    apt_info = {}
    '''
    return apt_info

def parse_bldgInfo():
    pass
