from src.query import get_buildings, get_apartments
from src.db_ops import create_connection, create_apt_table, add_apt

# Main scraping function
def main():
    # Initial testing url - update later as an argument
    page_url = 'https://www.apartments.com/detroit-mi/'

    # Get all apartment buildings in the specified query
    bldgs = get_buildings(base_url=page_url, num_pages=1)

    # Create a connection to the database
    db_path = '../data/scrape.db'
    conn = create_connection(db_path)

    create_apt_table(conn) # Create apt table if it doesn't exist

    # For each apartment building, extract all available apartment units
    # and add their information to the 'apts' table in the db
    for name,bldg_url in bldgs.items():
        apt_info = get_apartments(bldg_url)
        for apt in apt_info:
            add_apt(conn, apt)
if __name__ == '__main__':
    main()
