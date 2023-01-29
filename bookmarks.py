import sys
import json
import os

SEPARATOR = ' > '

query = sys.argv[1]
query_args = query.split(SEPARATOR)

bookmarks_json = None

def create_item(bookmark):
    is_folder = bookmark.get('type','') == 'folder'
    item = {}
    item["type"] = "default"
    item["uid"] = bookmark.get('guid')
    item["title"] = bookmark.get('name')
    item["arg"] = bookmark.get('url') or ''
    item["subtitle"] = bookmark.get('url') or 'Folder'
    item["autocomplete"] = bookmark.get('name') if not is_folder else bookmark.get("name") + SEPARATOR
    item["valid"] = not is_folder
    item["icon"] = { "path": "./folder.png" if is_folder else "./link.png" }

    return item

def is_match(query, bookmark):
    if not query:
        return True
    if query.lower() in bookmark.get('name', '').lower():
        return True
    return False

file_to_open = os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 2/Bookmarks')
with open(file_to_open) as file:
    bookmarks_json = json.load(file)
    
bookmarks = bookmarks_json['roots']['bookmark_bar']['children']
specific_query = query_args and query_args[-1]

for i in range(1, len(query_args)):
    bookmarks = next(sub_bookmarks for sub_bookmarks in bookmarks if sub_bookmarks["name"] == query_args[i-1])
    bookmarks = bookmarks['children']

output_list = [create_item(bookmark) for bookmark in bookmarks if is_match(specific_query, bookmark)]

output = {"items": output_list}
sys.stdout.write(json.dumps(output))