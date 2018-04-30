import functions.converter as convert
import functions.txt_updater as live_update

import config

from time import sleep
from requests import get
import json
import csv


steam_id = config.steam_ID
game_id = config.game_stream_ID
live_logging = config.live_logging
output_type = config.output_type
try_count = 0
current = None
previous = None
latest_run = {
    "timestamp": None
}


url = "https://tb-api.xyz/stream/get?s={steam}&key={game}".format(
    steam=steam_id,
    game=game_id
)


def update(run):
    if run:
        if output_type == "json":
            with open("data/data.json", "r") as file:
                data = json.load(file)

            for run_object in data:
                if run_object["timestamp"] == run["timestamp"]:
                    print("Already logged")
                    return
            print("Adding to data file")
            data.append(convert.JSON(run))

            with open("data/data.json", "w") as file:
                file.write(json.dumps(data, indent=2))


while True:
    print("=== Getting Data ===") #TODO: Remove when done debugging

    # Get the data from the API
    info = get(url).json()
    current = info["current"]
    previous = info["previous"]



    # Ensure that data actually exists
    if (not current) and (not previous):

        # Check to see that we haven't surpassed the three retry attempts
        if try_count >= 3:
            print("Make sure that you have the Stream Key enabled in your game settings then restart the logging.\nToo many failed data retrival attempts.")
            break



        # User confirmation
        cont = input("I have detected a lack of information (Make sure that your Stream Key is enabled in the game), would you like me to continue logging? (Y/N) ").lower()
        print("==========================") # NOTE: Leaving here as a separator

        # We are continueing logging
        if cont in ["y", "yes"]:
            try_count += 1
            pass

        # We're stopping the logger
        elif cont in ["n", "no"]:
            break

        # Invalid user input
        else:
            raise Error("Invalid input entry.")

    # See if we have a previous run to log.
    if previous:
        print("Logging Previous Run") # TODO: Remove when done debugging
        latest_run["timestamp"] = None
        update(previous)

    
    # Check if we are logging live
    if (live_logging and current):
        print("Updating live info")
        live_update.update_txt(current)


    # Wait 15 seconds for it to update again
    print("====================") # TODO: Remove when done debugging
    sleep(15)