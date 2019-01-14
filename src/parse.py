import re

def parse_availTable(table, bldg_id):
    # Parse the available units on a given apartment buildings dedicated page
    apt_info = []
    apts = table.find_all('tr', {'class': 'rentalGridRow'})
    for apt in apts:
        info = {}
        rentalkey = parse_rentalkey(apt)
        min_rent, max_rent = parse_rent(apt)
        beds = parse_beds(apt)
        baths = parse_baths(apt)
        min_area, max_area = parse_area(apt)

        info['rentalkey'] = rentalkey
        info['bldg_id'] = bldg_id
        info['min_rent'] = min_rent
        info['max_rent'] = max_rent
        info['beds'] = beds
        info['baths'] = baths
        info['min_area'] = min_area
        info['max_area'] = max_area

        apt_info.append(info)

    return apt_info

def parse_rentalkey(apt):
    # Extract the unique rentalkey (ID)
    return apt['data-rentalkey']

def parse_rent(apt):
    '''
    Extract the rental rate - slightly complicated because some units are
    listed with a high and low price
    :param apt: BeautifulSoup object for the specific apartment
    :return: min and max rent
    '''
    try:
        rent = apt.find('td', {'class': 'rent'}).get_text()
        rent = re.sub('[$,]', '', rent)

        # If rent is provided as a range
        if '-' in rent:
            min_rent, max_rent = rent.split('-')
            min_rent = int(min_rent)
            max_rent = int(max_rent)

        # if rent is a single value, set min = max
        else:
            min_rent, max_rent = int(rent), int(rent)
    except:
        # Some units have no rent listed
        return ('NA', 'NA')

    return (min_rent, max_rent)

def parse_beds(apt):
    # Extract the number of bedrooms
    try:
        beds = apt.find('td', {'class': 'beds'})
        beds = beds.find('span', {'class': 'shortText'}).get_text()
    except:
        return 'NA'

    return beds.strip()

def parse_baths(apt):
    # Extract the number of bathrooms
    try:
        baths = apt.find('td', {'class': 'baths'})
        baths = baths.find('span', {'class': 'shortText'}).get_text()
    except:
        return 'NA'

    return baths.strip()

def parse_area(apt):
    # Extract square footage
    try:
        area = apt.find('td', {'class': 'sqft'}).get_text()
        area = re.sub('[SqFt]', '', area)
        if '-' in area:
            min_area, max_area = area.split('-')
            min_area = int(min_area)
            max_area = int(max_area)
        else:
            min_area, max_area = int(area), int(area)
    except:
        return ('NA', 'NA')

    return (min_area, max_area)

def parse_bldgInfo(soup):
    # TODO
    return None
