import json
import os

data_file = "tournament_data.json"

def load_data():
    with open(data_file, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

def add_teams():
    data = load_data()
    print("Enter team names (leave empty to stop):")
    while True:
        name = input("Team: ").strip()
        if not name:
            break
        if name in data['teams']:
            print("Team already added.")
        else:
            data['teams'].append(name)
    save_data(data)
