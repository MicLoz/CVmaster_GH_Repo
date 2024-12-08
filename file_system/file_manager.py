import json

FILE_PATH = 'data/job_sites.json'
SEARCH_TERMS = 'data/search_terms.json'
WEB_DETAILS = 'data/job_sites_web_details.json'
CV_PATHS = 'data/cv_paths.json'

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
