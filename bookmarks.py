import sys
import json
import os

query = sys.argv[1]

bookmarks_json = None

def create_item(bookmark):
    item = {}
    item["type"] = "default"
    item["uid"] = bookmark.get('guid')
    item["title"] = bookmark.get('name')
    item["arg"] = bookmark.get('url') or 'https://www.google.com/'
    item["subtitle"] = bookmark.get('url') or 'Folder'
    item["autocomplete"] = bookmark.get('name')
    return item

file_to_open = os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 2/Bookmarks')
with open(file_to_open) as file:
    bookmarks_json = json.load(file)
    
bookmarks = bookmarks_json['roots']['bookmark_bar']['children']
# folders = [bookmark for bookmark in bookmarks if bookmark['type'] == 'folder']

def autocomplete_predicate(query, bookmark):
    if not query:
        return True
    if query.lower() in bookmark.get('name', '').lower():
        return True
    return False
output_list = [create_item(bookmark) for bookmark in bookmarks if autocomplete_predicate(query, bookmark)]

output = {"items": output_list}
sys.stdout.write(json.dumps(output))