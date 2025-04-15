import json
import os

DATA_FILE = "data.json"

def load_projects():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_projects(projects):
    with open(DATA_FILE, "w") as file:
        json.dump(projects, file, indent=4)
