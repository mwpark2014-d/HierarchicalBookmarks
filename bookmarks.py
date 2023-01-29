import sys
import json
import os

query = sys.argv[1]

bookmarks_json = None

file_to_open = os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 2/Bookmarks')
with open(file_to_open) as file:
    bookmarks_json = json.load(file)
    print(bookmarks_json)
    
bookmarks = bookmarks_json['roots']['bookmark_bar']['children']
folders = [bookmark for bookmark in bookmarks if bookmark['type'] == 'folder']
print(folders)

def create_item(title, link="google.com", subtitle=None):
	item = {}
	item["type"] = "default"
	item["title"] = title
	item["arg"] = link
	item["subtitle"] = subtitle
	item["autocomplete"] = title
	return item

q = {"items": [create_item(query)]}
j = json.dumps(q)
print(j)
sys.stdout.write(j)