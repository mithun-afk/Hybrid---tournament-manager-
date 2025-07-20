import os
import json
from teams import add_teams
from fixtures import generate_round_robin, generate_knockout
from results import enter_results
from points_table import show_points_table

def init_data():
    if not os.path.exists("tournament_data.json"):
        with open("tournament_data.json", 'w') as f:
            json.dump({"teams": [], "matches": [], "results": [], "phase": ""}, f, indent=4)

def load_data():
    with open("tournament_data.json", 'r') as f:
        return json.load(f)

def save_data(data):
    with open("tournament_data.json", 'w') as f:
        json.dump(data, f, indent=4)

def choose_format():
    data = load_data()
    n = len(data['teams'])
    print("Choose tournament format:")
    print("1. Round Robin")
    print("2. Knockout")
    choice = input("Select (1/2): ")
    if choice == '2' or n < 4:
        print("Using knockout mode.")
        data['phase'] = 'knockout'
        data['matches'] = generate_knockout(data['teams'])
    else:
        mode = input("Each team plays once or twice against each other? (1/2): ")
        double = mode.strip() == '2'
        data['phase'] = 'round_robin'
        data['matches'] = generate_round_robin(data['teams'], double)
    save_data(data)

def proceed_to_knockout():
    data = load_data()
    if data['phase'] == 'round_robin':
        top4 = show_points_table()[:4]
        print("\nTop 4 teams qualified for Knockouts:")
        for i, t in enumerate(top4, 1):
            print(f"{i}. {t}")
        semifinal_matches = [
            {"team1": top4[0], "team2": top4[3], "score1": None, "score2": None},
            {"team1": top4[1], "team2": top4[2], "score1": None, "score2": None},
        ]
        data['matches'] = semifinal_matches
        data['phase'] = 'semifinals'
        save_data(data)

def play_finals():
    data = load_data()
    if data['phase'] != 'semifinals':
        print("Finals can only be played after semifinals.")
        return

    pending = [m for m in data['matches'] if m['score1'] is None]
    if pending:
        print("Please enter all semifinal match results first.")
        return

    winners = []
    for match in data['matches']:
        if match['score1'] > match['score2']:
            winners.append(match['team1'])
        else:
            winners.append(match['team2'])

    print(f"\nFinal Match: {winners[0]} vs {winners[1]}")
    s1 = int(input(f"{winners[0]} score: "))
    s2 = int(input(f"{winners[1]} score: "))

    winner = winners[0] if s1 > s2 else winners[1]
    print(f"\n🏆 The Winner of the Tournament is: {winner} 🎉")
    data['phase'] = 'finished'
    save_data(data)

def menu():
    init_data()
    while True:
        print("\n--- Tournament Manager ---")
        print("1. Add Teams")
        print("2. Choose Format / Generate Fixtures")
        print("3. Enter Match Results")
        print("4. Show Points Table")
        print("5. Proceed to Knockouts (Top 4)")
        print("6. Play Final & Announce Winner")
        print("0. Exit")
        ch = input("Select: ")
        if ch == '1':
            add_teams()
        elif ch == '2':
            choose_format()
        elif ch == '3':
            enter_results()
        elif ch == '4':
            show_points_table()
        elif ch == '5':
            proceed_to_knockout()
        elif ch == '6':
            play_finals()
        elif ch == '0':
            print("Exiting Tournament Manager.")
            break
        else:
            print("Invalid option.")

menu()
