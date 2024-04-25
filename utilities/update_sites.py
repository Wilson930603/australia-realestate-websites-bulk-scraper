import json
from crawldata.helpers.database import Database


db = Database()
data = json.load(open('sites.json', 'r'))
listings = data.get('listings', [])
for key, value in listings.items():
    print("Updating site: " + key)
    db.update_sites(key, value)
sub_listings = data.get('sub_listings', [])
for key, value in sub_listings.items():
    print("Updating sub site: " + key)
    db.update_sub_sites(key, value)
