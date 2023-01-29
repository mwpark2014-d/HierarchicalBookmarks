import sys
import json
import os

SEPARATOR = ' > '

query = sys.argv[1]
query_args = query.split(SEPARATOR)

bookmarks_json = None

def create_item(bookmark):
    is_folder = bookmark.get('type','') == 'folder'

    autocomplete = bookmark.get('name') 
    if is_folder:
        subqueries = query_args[0:-1]
        subqueries.append(bookmark.get('name'))
        autocomplete = SEPARATOR.join(subqueries) + SEPARATOR

    item = {}
    item["type"] = "default"
    item["uid"] = bookmark.get('guid')
    item["title"] = bookmark.get('name')
    item["arg"] = bookmark.get('url') or ''
    item["subtitle"] = bookmark.get('url') or 'Folder'
    item["autocomplete"] = autocomplete
    item["valid"] = not is_folder
    item["icon"] = { "path": "./folder.png" if is_folder else "./link.png" }

    return item

def get_children(bookmarks, sub_query):
    new_bkmrks_obj = next(sub_bookmarks for sub_bookmarks in bookmarks if sub_bookmarks["name"] == sub_query)
    new_bkmrks_list = new_bkmrks_obj['children']
    return new_bkmrks_list

def is_match(query, bookmark):
    substrings = query.split(' ')
    if not query:
        return True
    for substring in substrings:
        if substring.lower() in bookmark.get('name', '').lower():
            return True
    return False

file_to_open = os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 2/Bookmarks')
with open(file_to_open) as file:
    bookmarks_json = json.load(file)
    
bookmarks = bookmarks_json['roots']['bookmark_bar']['children']
specific_query = query_args and query_args[-1]
log = specific_query

for i in range(1, len(query_args)):
    bookmarks = get_children(bookmarks, query_args[i-1])

bookmarks = sorted(bookmarks, key=lambda mark:mark.get('type'))
output_list = [create_item(bookmark) for bookmark in bookmarks if is_match(specific_query, bookmark)]

output = {"items": output_list}
sys.stdout.write(json.dumps(output))