import requests
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import time
from argparse import ArgumentParser

site = "https://grabify.link/api/domains?r=124"

headers = requests.request(method="get",url=site,headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br, zstd",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0",
    "Host":"grabify.link",
    "Accept-Language":"en-US,en;q=0.5",
    "Connection":"keep-alive"
    })

def site_main():
    # Parse commandline args
    parser = ArgumentParser(description="DeGrabify webcrawler")
    parser.add_argument("-d", "--database", dest="database",
                        help="path to the database", metavar="FILE", default="sites.json")
    parser.add_argument("-c", "--cron", dest="cron",
                        help="cronjob for the crawler (default once per day @ noon)", metavar="CRON", default="0 12 * * *")
    args = parser.parse_args()
    db_path = args.database.strip()
    cron = args.cron

    # Loop fetching domain list
    print("Fetching domains...")
    sites=get_domains()
    if sites is not None:
        print("Got domains")
        store_sites(sites, db_path)
    else:
        print(f"Failed to fetch domains from {site}")

def get_domains():
    resp = requests.get(site)
    if not resp.ok:
        print(f"Error fetching list': {resp.status_code} error")
        #print(resp.text)
        return None
    return resp.json()

def store_sites(sites, db_path:str):
    print(f"Saving {len(sites)} domains to database at path \"{db_path}\"")

    with TinyDB(
        db_path, 
        storage=CachingMiddleware(JSONStorage), 
        sort_keys=True, 
        indent=4, 
        separators=(',', ': ')
    ) as db:

        Site = Query()
        Update = Query()

        sites_table = db.table("sites")
        updated = db.table("lastUpdated")

        updated.truncate()
        
        for site in sites:
            sites_table.upsert(site, Site.Domain == site["Domain"])

        updated.insert({"lastUpdated":time.asctime()})

    print("Done saving domains")

        

if __name__ == "__main__":
    print("Crawler init")
    site_main()
    print()