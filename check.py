import json
from config import PATHS

def check_categories(json_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
        all_categories = set()
        for img in data:
            for label in img.get('labels', []):
                all_categories.add(label['category'])
        print("Categories in JSON:", all_categories)

check_categories(PATHS['labels_path_json_train'])
