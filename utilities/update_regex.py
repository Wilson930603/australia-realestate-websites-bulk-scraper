from crawldata.helpers.utils import load_regex
from crawldata.helpers.database import Database


db = Database()
regex_list = load_regex()
for key, value in regex_list.items():
    print("Updating regex: " + key)
    value['website'] = key
    db.insert_regex_points(value)
