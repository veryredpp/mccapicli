import requests
import pprint
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


def main():
    url = "https://api.mcchampionship.com"

    parameters = {}
    teams = ["RED", "ORANGE", "YELLOW", "LIME", "GREEN", "AQUA", "CYAN", "BLUE", "PURPLE", "PINK", "SPECTATORS", "NONE"]

    selection_types = ["Event Information", "Hall of Fame", "Event Rundown", "Participants"]
    prompt = inquirer.prompt([inquirer.List("selection", message='MCC Event API CLI', choices=selection_types)])
    selection = prompt["selection"]

    if selection == "Event Information":
        response = requests.get(url + "/v1/event")

        # event name
        event_name = response.json().get('data').get('event')
        print(f"Event: {event_name}")

        # fix unreadable date-time format
        date_str = response.json().get('data').get('date')
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date = date_obj.strftime("%B %d, %Y %I:%M %p")
        print(f"Date: {formatted_date}")

        # Check for None reply
        update_video = response.json().get('data').get('updateVideo')
        if update_video == "None":  # none is a bit vague
            update_video = "Not released"
        print(f"Updated Video: {update_video}")

    elif selection == 3:
        response = requests.get(url + "/v1/rundown")
        dodgeboltdata = response.json().get('data').get('dodgeboltData')
        dodgeboltkeys = list(dodgeboltdata.keys())
        dodgeboltkeys.remove("placeholder")
        print("\nDodgebolt:")
        print(
            f"    {dodgeboltkeys[0]} {dodgeboltdata[dodgeboltkeys[0]]}-{dodgeboltdata[dodgeboltkeys[1]]} {dodgeboltkeys[1]}\n")
        teamsplaces = []
        for i in teams:
            teamsplaces.append(response.json().get('data').get('eventPlacements').get(i))
        for i in range(2):
            teamsplaces.remove(None)
        teamsplaces.sort()
        print("Placements:")
        for i in teamsplaces:
            for j in teams:
                if response.json().get('data').get('eventPlacements').get(j) == i:
                    print(f"{i + 1}. {j}  {response.json().get('data').get('eventScores').get(j)}")
        playerscoredata = response.json().get('data').get('individualScores')
        playerscorekeys = list(playerscoredata.keys())
        print("\nIndividual Scores:")
        playerscore = []
        for i in playerscorekeys:
            playerscore.append(playerscoredata[i])
        playerscore.sort(reverse=True)
        counter = 0
        for i in playerscore:
            for j in playerscorekeys:
                if i == response.json().get('data').get('individualScores').get(j):
                    counter += 1
                    print(f"{counter}. {j}  {i}")

    elif selection == 4:
        print("\n1. All of the participants, grouped by their teams\n2. Participants in a given team")
        selection2 = int(input("Select -> "))
        if selection2 == 1:
            response = requests.get(url + "/v1/participants")
            for i in teams:
                temp_list = response.json().get('data').get(i)
                print(i + ":")
                for j in range(len(temp_list)):
                    print(" " + temp_list[j].get('username'))
        elif selection2 == 2:
            print(
                "\nSpectators and None are considered teams. For a full list of the teams write '?' without quotes below. Type in ALL CAPS.")
            team = input("Select Team -> ")
            while team == "?":
                print(
                    "\nAvailable values :\n RED\n ORANGE\n YELLOW\n LIME\n GREEN\n AQUA\n CYAN\n BLUE\n PURPLE\n PINK\n SPECTATORS\n NONE")
                team = input("Select Team -> ")
            parameters["team"] = team
            response = requests.get(url + "/v1/participants" + "/" + parameters["team"], params=parameters)
            temp_list = response.json().get('data')
            print("\n" + team + ":")
            for i in range(len(temp_list)):
                print(" " + temp_list[i].get('username'))
    print("\n\n")


if __name__ == "__main__":
    main()
