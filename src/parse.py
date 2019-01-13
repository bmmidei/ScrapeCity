import re

def parse_availTable(table):
    # Parse the available units on a given apartment buildings dedicated page
    apt_info = []
    apts = table.find_all('tr', {'class': 'rentalGridRow'})
    for apt in apts:
        info = {}
        min_rent, max_rent = parse_rent(apt)
        beds = parse_beds(apt)
        baths = parse_baths(apt)
        min_area, max_area = parse_area(apt)

        info['min_rent'] = min_rent
        info['max_rent'] = max_rent
        info['beds'] = beds
        info['baths'] = baths
        info['min_area'] = min_area
        info['max_area'] = max_area

        apt_info.append(info)

    return apt_info


def parse_rent(apt):
    try:
        rent = apt.find('td', {'class': 'rent'}).get_text()
        rent = re.sub('[$,]', '', rent)
        if '-' in rent:
            min_rent, max_rent = rent.split('-')
            min_rent = int(min_rent)
            max_rent = int(max_rent)
        else:
            min_rent, max_rent = int(rent), int(rent)
    except:
        return ('NA', 'NA')

    return (min_rent, max_rent)


def parse_beds(apt):
    try:
        beds = apt.find('td', {'class': 'beds'})
        beds = beds.find('span', {'class': 'shortText'}).get_text()
    except:
        return 'NA'

    return beds.strip()


def parse_baths(apt):
    try:
        baths = apt.find('td', {'class': 'baths'})
        baths = baths.find('span', {'class': 'shortText'}).get_text()
    except:
        return 'NA'

    return baths.strip()


def parse_area(apt):
    try:
        area = apt.find('td', {'class': 'sqft'}).get_text()
        area = re.sub('[SqFt]', '', area)
        if '-' in area:
            min_area, max_area = area.split('-')
            min_area = int(min_area)
            max_area = int(max_area)
        else:
            min_area, max_area = int(min_area), int(max_area)
    except:
        return ('NA', 'NA')

    return (min_area, max_area)


def parse_bldgInfo():
    pass