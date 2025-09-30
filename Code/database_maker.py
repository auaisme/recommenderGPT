
from dotenv import load_dotenv
import requests, os, json

all_apps = None

load_dotenv()

def store_as_json(data, path: str, encoding: str = "utf-8"):
    existing_list = []

    try:
        with open(path, "r", encoding=encoding) as file:
            existing_list = json.load(file)  # assuming it's a list
    except:
        print(f'Error occurred while opening file')
        input("Press any key to continue (will replace any existing data)")
    finally:
        # Append new items
        existing_list.extend(data)
        with open(path, "w", encoding=encoding) as file:
            json.dump(
                existing_list,
                file,
                ensure_ascii=False,
                indent=2 
            )
    return

def get_all_apps():
    response = requests.get(
        url=os.environ["GET_ALL_GAMES_URL"]
    )

    if response.ok:
        all_apps = response.json()["applist"]["apps"]
        # print(type(all_apps))
        # print(all_apps)
        store_as_json(all_apps, "all_apps_on_steam.json")
        print("Done!")
    return


