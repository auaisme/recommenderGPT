# import requests
# from bs4 import BeautifulSoup

# url = "https://www.ign.com/articles/2018/05/24/detroit-become-human-review"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                   "AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/115.0 Safari/537.36"
# }

# print(f"Hitting {url}\nHeaders {headers}")

# response = requests.get(url, headers=headers)

# print(response)
# print(response.text)

# soup = BeautifulSoup(response.text, "html.parser")

# # Find "inner" class inside "outer" class
# # results = soup.select(".article .jsx-3932497636")  
# results = soup.select(".article-page p.paragraph")

# print(results)
# input("Continue?")

# for div in results:
#     print(div.get_text(strip=True))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

def format_game_name(name: str) -> str:
    formated = ""
    name = name.lower()
    for c in name:
        if (c < 'a' or c > 'z') and c != ' ' and (c < '0' or c > '9'):
            continue
        if (c == ' '):
            formated = formated + '-'
        else:
            formated = formated + c
    return formated

def setup_browser(timeout_in_seconds: int = 5, background: bool = False):
    # Setup Chrome
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    if background:
        options.add_argument("--headless")  # run in background (remove if you want to see the browser)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print("Setting timeout")
    driver.set_page_load_timeout(timeout_in_seconds)
    print("Timeout set")
    return driver

def scrape(game_name: str, driver, close_driver: bool = False):
    result = ""
    try:
        url = f"https://www.ign.com/articles/{game_name}-review"
        try:
            driver.get(url)
        except TimeoutException:
            print("⚠️ Page load timed out, continuing anyway...")
        except WebDriverException as e:
            print(f"⚠️ WebDriver error occurred: {e}")
            try:
                url = f"https://www.ign.com/articles/{game_name}"
                driver.get(url)
            except TimeoutException:
                print("⚠️ Page load timed out, continuing anyway...")
            except WebDriverException as e:
                print(f"NEITHER URLS WORKED ⚠️ WebDriver error occurred: {e}")
                return result
            except Exception as e:
                print(f"NEITHER URLS WORKED ⚠️ error occurred: {e}")
                return result
        except Exception as e:
            print(f"⚠️ Some other error occurred: {e}")
            try:
                url = f"https://www.ign.com/articles/{game_name}"
                driver.get(url)
            except TimeoutException:
                print("⚠️ Page load timed out, continuing anyway...")
            except WebDriverException as e:
                print(f"NEITHER URLS WORKED ⚠️ WebDriver error occurred: {e}")
                return result
            except Exception as e:
                print(f"NEITHER URLS WORKED ⚠️ error occurred: {e}")
                return result
        print("Post get")

        # ✅ Wait until paragraphs are present
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "p[data-cy='paragraph']"))
        # )

        # Grab all matching elements
        # results = driver.find_elements(By.CSS_SELECTOR, "p[data-cy='paragraph']")

        # Find the container
        article_container = driver.find_element(By.CSS_SELECTOR, ".article-page")
        verdict = driver.find_element(By.CSS_SELECTOR, "[data-cy=verdict]")

        # Get *all* text inside, including bare strings and paragraphs
        result = article_container.text + "\n" + verdict.text
        # print(result)
    finally:
        if close_driver:
            driver.quit()
        return result

def store_as_json(data, path: str, encoding: str = "utf-8"):
    with open(path, "r", encoding=encoding) as file:
        existing_list = json.load(file)  # assuming it's a list

    # Append new items
    existing_list.extend(data)

    with open(path, "w", encoding=encoding) as file:
        json.dump(
            existing_list,
            file,
            ensure_ascii=False,
            indent=2 
        )
    pass

def split_into_chunks(
    data: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    length_function: callable = len,
    separators: list[str] = ["\n\n", "\n", ". ", "; ", ", ", " ", ""]
):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function,
        separators=separators,  # try to split nicely
    )
    chunks = text_splitter.split_text(data)
    return chunks

def get_review(
    game_names: list[str],
    log: bool = False,
    show_browser: bool = False,
    timeout_in_seconds=15,
    chunkify: bool = True,
    store_in_json: bool = False
):
    result = ""
    games_reviews_map = []

    for name in game_names:
        games_reviews_map.append({
            "title": name,
            "review": "",
            "source": ""
        })

    driver = setup_browser(timeout_in_seconds=timeout_in_seconds, background=not show_browser)

    i: int = 0
    for name in game_names:
        print(f"Scraping {name}")
        result = scrape(game_name=format_game_name(name=name), driver=driver)
        print(len(result))
        games_reviews_map[i]["review"] = result
        games_reviews_map[i]["source"] = "ign"
        print(f"Done")
        i = i + 1
    driver.quit()

    if store_in_json:
        print(f"Storing")
        store_as_json(data=games_reviews_map, path="reviews.json")
        pass

    if not chunkify:
        return games_reviews_map

    all_chunks = []

    for review in games_reviews_map:
        chunks = split_into_chunks(data=review["review"])
        print(f"Chunks count: {len(chunks)}")
        all_chunks.append(
            {
                "title": review["title"],
                "chunks": chunks
            }
        )

    if log:
        from rich import print_json
        print_json(data=all_chunks)
    
    return all_chunks

# games = [
#     "The Legend of Zelda: Breath of the Wild",
#     "Elden Ring",
#     "God of War Ragnarok",
#     "Cyberpunk 2077",
#     "Red Dead Redemption 2"
#     "Ghost of Tsushima",
#     "Deltarune",
# ]

games_list = [
    "Tetris",
    "The Legend of Zelda: Ocarina of Time",
    "Super Mario 64",
    "Half-Life 2",
    "Resident Evil 4",
    "The Last of Us",
    "The Witcher III: Wild Hunt",
    "Super Mario World",
    "Shadow of the Colossus",
    "Final Fantasy VII",
    "Doom",
    "Mass Effect 2",
    "Super Metroid",
    "Super Mario Bros.",
    "Bioshock",
    "The Elder Scrolls V: Skyrim",
    "The Legend of Zelda: A Link to the Past",
    "Red Dead Redemption",
    "Metal Gear Solid",
    "Diablo II",
    "Chrono Trigger",
    "Portal 2",
    "Uncharted 2: Among Thieves",
    "The Sims 3",
    "Halo: Combat Evolved",
    "World of Warcraft",
    "Grand Theft Auto V",
    "Final Fantasy X",
    "Persona 5",
    "Bloodborne",
    "Overwatch",
    "Minecraft",
    "The Elder Scrolls III: Morrowind",
    "Batman: Arkham City",
    "Metal Gear Solid 3: Snake Eater",
    "Super Mario Odyssey",
    "The Witcher 2: Assassins of Kings",
    "Final Fantasy VI",
    "The Last of Us Part II",
    "The Legend of Zelda: Majora's Mask",
    "Dark Souls III",
    "Hollow Knight",
    "Nier: Automata",
    "Persona 4 Golden",
    "Final Fantasy IX",
    "The Elder Scrolls IV: Oblivion",
    "The Legend of Zelda: Twilight Princess",
    "God of War",
    "Grand Theft Auto IV",
    "Bioshock Infinite",
    "Uncharted: Drake's Fortune",
    "Assassin's Creed II",
    "Dark Souls II",
    "Final Fantasy XV",
    "The Legend of Zelda: Wind Waker",
    "Halo 3",
    "Mass Effect",
    "The Sims 4",
    "Dark Souls",
    "The Legend of Zelda: Phantom Hourglass",
    "God of War III",
    "Uncharted 3: Drake's Deception",
    "Metal Gear Solid V: The Phantom Pain",
    "The Elder Scrolls Online",
    "Final Fantasy XIV",
    "The Legend of Zelda: Link's Awakening",
    "Uncharted 4: A Thief's End",
    "Metal Gear Solid: Peace Walker",
    "Grand Theft Auto: Vice City",
    "Grand Theft Auto: San Andreas",
    "Final Fantasy XIV: Heavensward",
    "The Sims 2",
    "The Legend of Zelda: Skyward Sword",
    "God of War: Chains of Olympus",
    "Metal Gear Solid: Ground Zeroes",
    "Grand Theft Auto: Liberty City Stories",
    "Final Fantasy XIV: Shadowbringers",
    "The Sims 3"
]

get_review(games_list, log=True, show_browser=False, timeout_in_seconds=10, store_in_json=True)
