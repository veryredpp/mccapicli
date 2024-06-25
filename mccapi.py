import requests
from pprint import pprint
import inquirer
import datetime

games = {
    "Rocket Spleef": "MG_ROCKET_SPLEEF",
    "Survival Games": "MG_SURVIVAL_GAMES",
    "Parkour Warrior": "MG_PARKOUR_WARRIOR",
    "Ace Race": "MG_ACE_RACE",
    "Bingo But Fast": "MG_BINGO_BUT_FAST",
    "TGTTOSAWAF": "MG_TGTTOSAWAF",
    "TGTTOS": "MG_TGTTOSAWAF",
    "To Get To The Other Side": "MG_TGTTOSAWAF",
    "To Get To The Other Side And Whack A Fan": "MG_TGTTOSAWAF",
    "Skyblockle": "MG_SKYBLOCKLE",
    "Sky Battle": "MG_SKY_BATTLE",
    "SB": "MG_SKY_BATTLE",
    "Hole In The Wall": "MG_HOLE_IN_THE_WALL",
    "HITW": "MG_HOLE_IN_THE_WALL",
    "Battle Box": "MG_BATTLE_BOX",
    "BB": "MG_BATTLE_BOX",
    "Build Mart": "MG_BUILD_MART",
    "BM": "MG_BUILD_MART",
    "Sands of Time": "MG_SANDS_OF_TIME",
    "Sands Of Time": "MG_SANDS_OF_TIME",
    "SOT": "MG_SANDS_OF_TIME",
    "Dodgebolt": "MG_DODGEBOLT",
    "DB": "MG_DODGEBOLT",
    "Parkour Tag": "MG_PARKOUR_TAG",
    "PT": "MG_PARKOUR_TAG",
    "Grid Runners": "MG_GRID_RUNNERS",
    "GR": "MG_GRID_RUNNERS",
    "MELTDOWN": "MD_MELTDOWN",
    "MD": "MD_MELTDOWN"

}


def main() -> int:
    url = "https://api.mcchampionship.com"

    parameters = {}
    teams = ["RED", "ORANGE", "YELLOW", "LIME", "GREEN", "AQUA", "CYAN", "BLUE", "PURPLE", "PINK", "SPECTATORS", "NONE"]

    # make requests beforehand
    response_event_info = requests.get(url + "/v1/event")
    response_event_rundown = requests.get(url + "/v1/rundown")
    response_participants = requests.get(url + "/v1/participants")

    selection_types = ["Event Information", "Event Rundown", "Participants", "Exit"]
    prompt = inquirer.prompt([inquirer.List("selection", message='MCC Event API CLI', choices=selection_types)])
    selection = prompt["selection"]

    if selection == "Event Information":
        # event name
        event_name = response_event_info.json().get('data').get('event')
        print(f"Event: {event_name}")

        # fix unreadable date-time format
        date_str = response_event_info.json().get('data').get('date')
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date = date_obj.strftime("%B %d, %Y %I:%M %p")
        print(f"Date: {formatted_date}")

        # Check for None reply
        update_video = response_event_info.json().get('data').get('updateVideo')
        if update_video == "None":  # none is a bit vague
            update_video = "Not released"
        print(f"Updated Video: {update_video}")

    elif selection == "Event Rundown":

        # dodgebolt score
        dodgebolt_data = response_event_rundown.json().get('data').get('dodgeboltData')
        dodgebolt_keys = list(dodgebolt_data.keys())
        print("\nDodgebolt:")
        print(f" {dodgebolt_keys[0]} {dodgebolt_data[dodgebolt_keys[0]]}-{dodgebolt_data[dodgebolt_keys[1]]} {dodgebolt_keys[1]}\n")

        # team leaderboards
        teams_places = []
        for team in teams:
            teams_places.append(response_event_rundown.json().get('data').get('eventPlacements').get(team))
        for i in range(2):
            teams_places.remove(None)
        teams_places.sort()
        print("Placements:")
        for team_place in teams_places:
            for team in teams:
                if response_event_rundown.json().get('data').get('eventPlacements').get(team) == team_place:
                    placement = team_place + 1
                    score = response_event_rundown.json()['data']['eventScores'][team]
                    print(f"{placement:2}. {team:<9}{score:>6}")

        # player scores
        player_score_data = response_event_rundown.json().get('data').get('individualScores')

        if "placeholder" in player_score_data:
            del player_score_data["placeholder"]

        print("\nIndividual Scores:")
        player_scores = [(player, score if score is not None else 0) for player, score in player_score_data.items()]
        player_scores.sort(key=lambda x: x[1], reverse=True)

        counter = 0
        for player, score in player_scores:
            counter += 1
            print(f"{counter:2}. {player:<15} {score}")

    elif selection == "Participants":
        selection_types2 = ["All of the participants, grouped by their teams", "Participants in a given team"]
        prompt2 = inquirer.prompt([inquirer.List("selection2", choices=selection_types2)])
        selection2 = prompt2["selection2"]

        participants_data = response_participants.json().get('data')

        # List of teams (keys in the participants data)
        teams = list(participants_data.keys())

        if selection2 == "All of the participants, grouped by their teams":
            for team, members in participants_data.items():
                print(f"{team}:")
                for member in members:
                    print(f"  {member.get('username')}")
                print()

        elif selection2 == "Participants in a given team":
            team_selection = inquirer.prompt([inquirer.List("team_selection", message="Choose Team", choices=teams)])
            team = team_selection['team']
            team_members = participants_data.get(team, [])
            print(f"\n{team}:")
            for member in team_members:
                print(f"  {member.get('username')}")

    elif selection == "Exit":
        return -1
    print("\n")


if __name__ == "__main__":
    while main() != -1:
        pass
    exit()
