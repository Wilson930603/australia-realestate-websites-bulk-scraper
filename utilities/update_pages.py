import json
from crawldata.helpers.database import Database


db = Database()
data = json.load(open('pages.json', 'r'))
for business_id, page in data.items():
    print("Updating site: " + business_id)
    db.update_pages(business_id, page)
