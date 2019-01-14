from bs4 import BeautifulSoup as BS
from src.parse import parse_availTable
import requests


def get_buildings(base_url, num_pages):
    '''
    Extract a list of apartment buildings and corresponding urls from a given
    Apartments.com query
    :param url: url of the first page of the query
    :param num_pages: number of pages of listings to search
    :return: A dictionary of apartment buildings and corresponding urls
    '''
    req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    page_url = base_url
    buildings = {}
    n=0 # Page counter
    while page_url is not None and n < num_pages:
        n += 1
        page = requests.get(page_url, headers=req_headers)
        soup = BS(page.content, 'html.parser')

        # Examine the placard containers. Each placard represents an apartment
        # building.
        headers = soup.find_all('header', {'class': 'placardHeader'})
        for header in headers:
            url = header.find('a', {'class': 'placardTitle'}).get('href')

            name = header.find('a', {'class': 'placardTitle'}).get('title')
            buildings[name] = url

        # Update url to the next page
        page_url = get_next_page(soup)

    # Return a dictionary of names and urls to each building's listings
    return buildings

def get_next_page(current_page):
    # Extract the url of the next page of listings
    soup = current_page.find('div', {'id': 'paging', 'class': 'paging'})
    next_url = soup.find('a', attrs={'class':'next', 'data-page': True}).get('href')
    if next_url == 'javascript:void(0)':
        # If there are no more pages of listings
        return None
    else:
        return next_url

def get_apartments(url):
    # For a given apartment building, extract the listing information for
    # the available units
    req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    page = requests.get(url, headers=req_headers)
    soup = BS(page.content, 'html.parser')

    # Extract the bldg id (unique to each apartment building)
    bldg_id = soup.find('main', attrs={'data-listingid':True})['data-listingid']

    # Examine the availability table
    table = soup.find("table", {"class": "availabilityTable"})
    apt_info = parse_availTable(table, bldg_id)

    return apt_info

'''
def building(url):
    req_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    page = requests.get(url, headers=req_headers)
    soup = BS(page.content, 'html.parser')
    #print(soup.prettify())
    #a = soup.find_all('main', recursive=False)
    #a = soup.find(attrs={'data-listingid':True}, recursive=False)
    element = soup.find('main', attrs={'data-listingid':True})['data-listingid']

'''