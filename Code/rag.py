# ------------------------------------------------- API  KEY ------------------------------------------------- 
# 
# open router (Demo API for Recommendor):
# 
# ------------------------------------------------- API  KEY -------------------------------------------------

from dotenv import load_dotenv
import requests, difflib, json, os

load_dotenv()

# API_KEY = LOAD FROM .ENV

def load_reviews(input_file):
    print("\nLoading reviews from local storage")
    # Read JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert list of {title, review, source} into {title: review}
    reviews_dict = {item['title']: item['review'] for item in data}

    return reviews_dict

def chat_with_openrouter(message, games, history=None, model="google/gemma-3-4b-it:free"):
    # TODO: Convert this into langchain

    if history is None:
        history = []

    message = "You are a system that reads reviews about products" + \
    " and your job is to tell me how similar are my checking" + \
    " products to my target product. You will give each checking" + \
    " product a rating on a scale of 0 to 100 with 100 showing that" + \
    " the products are identicle. You will also give a summary of your" + \
    " reasoning in a 3 line precis. For each product, you will" + \
    " be told whether it's a target product or a checking product." + \
    " you will give your results after I asks you for results with a message" + \
    " saying 'show results'. Say 'ok' in between messages to show that you" + \
    " are done working."

    # Add user message to the history
    history.append({"role": "user", "content": message})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,  # pick a free/cheap model
            "messages": history
        }
    )

    data = response.json()
    if "choices" in data:
        reply = data["choices"][0]["message"]["content"]
        # Add assistant reply to history
        history.append({"role": "assistant", "content": reply})
        print(reply)
    else:
        raise Exception(f"API error: {data}")
    
    i: int = 0
    for game, review in games.items():
        if i == 0:
            message = f'Target ({game}): "{review}"'
            print(f'Target: {game}')
            i = i + 1
        else:
            message = f'Checking {i} ({game}): "{review}"'
            print(f"Checking {i}: {game}")

        history.append({"role": "user", "content": message})

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,  # pick a free/cheap model
                "messages": history
            }
        )

        data = response.json()
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
            # Add assistant reply to history
            history.append({"role": "assistant", "content": reply})
            print(reply)
        else:
            raise Exception(f"API error: {data}")
        pass
    # end for
    return history
# end func

def identify_games(input_text, games_dict, similarity_threshold=0.8):
    input_lower = input_text.lower()
    found = {}

    # Exact substring matches
    for game, review in games_dict.items():
        if game.lower() in input_lower:
            print(game)
            # found.append((game, review))
            found[game] = review

    # If nothing matched exactly, try fuzzy match on the whole input
    if not found:
        best_matches = difflib.get_close_matches(
            input_text, games_dict.keys(), n=3, cutoff=similarity_threshold
        )
        for game in best_matches:
            print(game)
            # found.append((game, games_dict[game]))
            found[game] = games_dict[game]

    return found

# --- Example usage ---
def direct_request():
    history = []
    input_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scraper/reviews.json")
    games = load_reviews(input_path)
    # print(games)
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break
        matches = identify_games(user_input, games)
        history = chat_with_openrouter(message=user_input, games=matches, history=history, model="openai/gpt-4o")
        # print("Bot:", reply)

from langchain_openai import OpenAI
from langchain.chat_models import init_chat_model
from langchain import hub

# API2 = os.environ["OPENAI_API_KEY"] = 
# os.environ["OPENAI_API_KEY"] = str(os.getenv("OPEN_ROUTER_KEY"))
print("API: " + str(os.environ["OPENAI_API_KEY"]))

import sys
if os.environ["OPENAI_API_KEY"] == "" or os.environ["OPENAI_API_KEY"] == "None":
    print("ERROR: OPENAI API KEY IS NULL OR OF 0 LENGTH")
    sys.exit("CRITICAL ERROR")

os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

models = {
    "deepseek": {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "provider": "openai"
    },
    "gpt 3": {
        "model": "gpt-3.5-turbo",
        "provider": "openai"
    }
}

def summarize(games, comparison_games, prompt_factory, llm):
    summaries = {}
    print("\nSummarizing reviews")
    for game in comparison_games:
        prompt = prompt_factory.invoke({
            "question": f"Write a precis of '{game}' review: ",
            "context": games[game]
        })
        response = llm.invoke(prompt)
        summaries[game] = response.content
        print(f"{game}'s review summarized")
        # print(llm.invoke(prompt).content)
    # end loop
    return summaries
# end func

def langchain_implementation(comparison_games, model = "deepseek", summarize_flag: bool = False):
    llm = init_chat_model(model=models[model]["model"], model_provider=models[model]["provider"])

    input_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Scraper/reviews.json")
    games = load_reviews(input_path)
    # TODO Replace ^ with loading only relevant reviews

    prompt_factory = hub.pull("rlm/rag-prompt")

    summaries = {}
    if summarize_flag:
        summaries = summarize(games=games, comparison_games=comparison_games, llm=llm, prompt_factory=prompt_factory)
    else:
        for game in comparison_games:
            summaries[game] = games[game]
        # end for
    # end if

    # TODO Change the summarize logic to: summarize if the character limits exceed the max tokens

    target_game = comparison_games.pop(0)

    results= []
    print("\nComparing games")
    for game in comparison_games:
        prompt = prompt_factory.invoke({
            "question": f"By force, rate how similar {target_game} is to {game}, focusing on game design philosphy, mechanics, and target audience; on a scale of 1 through 100" + \
                " with 100 meaning they're identical. Also give a precis of your reasoning, and if you're lacking context, tell me. Split your response into your score and reasoning.",
            "context": [summaries[target_game], summaries[game]]
        })
        response = llm.invoke(prompt)
        result = f"{target_game} v {game}\n\n" + response.content + "\n\n"
        results.append(result)
        # print(result)
        print(f"Compared {target_game} to {game}")
        # end loop
    print("END")
    return results
# end function

compare_these = [
    # "Red Dead Redemption 2",
    "Undertale",
    "Deltarune",
    "Cyberpunk 2077",
    "Grand Theft Auto V",
    "Grand Theft Auto IV",
    "Red Dead Redemption"
]

results = langchain_implementation(comparison_games=compare_these, model="deepseek")

print("\n\n")
for result in results:
    print(result)
# end for loop
