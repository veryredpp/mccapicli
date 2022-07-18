import requests
import pprint
def main():
    url = "https://api.mcchampionship.com"

    parameters = {}
    print("MCC Event API")
    print("1. Event Information\n2. Hall of Fame\n3. Event Rundown\n4. Participants")
    selection = int(input("Select -> "))

    if selection == 1:
        response = requests.get(url + "/v1/event")
        pprint.pprint(response.json().get('data'))
    elif selection == 2:
        print("\n1. Entire Hall of Fame\n2. Hall of Fame for a specific game")
        selection2 = int(input("Select -> "))
        if selection2 == 1:
            response = requests.get(url + "/v1/halloffame")
            pprint.pprint(response.json().get('data'))
        elif selection2 == 2:
            print("\nIf you don't know the id values for the games type '?' without quotes below, Hint: Type a 'MG_' in the front and then the games name replacing its spaces with underscores (ALL CAPS).")
            game = input("Game ID -> ")
            while game == "?":
                print("\nAvailable values :\n MG_ROCKET_SPLEEF\n MG_SURVIVAL_GAMES\n MG_PARKOUR_WARRIOR\n MG_ACE_RACE\n MG_BINGO_BUT_FAST\n MG_TGTTOSAWAF\n MG_SKYBLOCKLE\n MG_SKY_BATTLE\n MG_HOLE_IN_THE_WALL\n MG_BATTLE_BOX\n MG_BUILD_MART\n MG_SANDS_OF_TIME\n MG_DODGEBOLT\n MG_PARKOUR_TAG\n MG_GRID_RUNNERS\n MG_MELTDOWN\n GLOBAL_STATISTICS\n LEGACY_STATISTICS")
                game = input("Enter game name -> ")
            parameters["game"] = game
            response = requests.get(url + "/v1/halloffame" + "/" + parameters["game"], params=parameters)
            pprint.pprint(response.json().get('data'))
    elif selection == 3:
        response = requests.get(url + "/v1/rundown")
        pprint.pprint(response.json().get('data'))
    elif selection == 4:
        print("\n1. All of the participants, grouped by their teams\n2. Participants in a given team")
        selection2 = int(input("Select -> "))
        if selection2 == 1:
            response = requests.get(url + "/v1/participants")
            pprint.pprint(response.json().get('data'))
        elif selection2 == 2:
            print("\nSpectators and None are considered teams. For a full list of the teams write '?' without quotes below. Type in ALL CAPS.")
            team = input("Select Team -> ")
            while team == "?":
                print("\nAvailable values :\n RED\n ORANGE\n YELLOW\n LIME\n GREEN\n AQUA\n CYAN\n BLUE\n PURPLE\n PINK\n SPECTATORS\n NONE")
                team = input("Select Team -> ")
            parameters["team"] = team
            response = requests.get(url + "/v1/participants" + "/" + parameters["team"], params=parameters)
            pprint.pprint(response.json().get('data'))
        
# I refuse to do normal methods, I don't care. While True is funny right? Right? RIGHT?    
while True:
    main()  # I'm not sure if this is the best way to do this, but it works.
    print("\n\n\n")