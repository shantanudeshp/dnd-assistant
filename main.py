import json
import re
import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras
import shutil

def load_game_state(file_path: str) -> dict:
    """Load the current game state from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_game_state(file_path: str, state: dict) -> None:
    """Save the updated game state to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(state, f, indent=2)

def reset_game_state(initial_file: str, current_file: str) -> None:
    """Reset the game state by copying the initial state to the current state."""
    shutil.copy(initial_file, current_file)
    print("Game has been reset to the initial state.\n")

def parse_llm_response(response: str) -> tuple:
    """
    Parses the LLM response to extract the narrative and updated game state.
    Assumes the updated game state is within a JSON code block.
    """
    narrative_match = re.search(
        r'\*\*Narrative\*\*:?[\n\s]+([\s\S]+?)\n\n\*\*Updated Game State\*\*:?', 
        response, 
        re.IGNORECASE
    )
    narrative = narrative_match.group(1).strip()

    game_state_match = re.search(
        r'```json\n([\s\S]+?)\n```', 
        response, 
        re.IGNORECASE
    )
    game_state_str = game_state_match.group(1).strip()
    updated_game_state = json.loads(game_state_str)

    return narrative, updated_game_state

def initialize_client() -> Cerebras:
    """Initialize the Cerebras client using the API key from the environment."""
    load_dotenv()
    api_key = os.environ.get("CEREBRAS_API_KEY")
    client = Cerebras(api_key=api_key)
    return client

def provide_initial_narrative(client: Cerebras, game_state: dict) -> dict:
    """Provide an initial narrative to start the game."""
    prompt = (
        "You are a Dungeons & Dragons (D&D) assistant managing the game state. Below is the current game state:\n\n"
        f"{json.dumps(game_state, indent=2)}\n\n"
        "Player's action: start\n\n"
        "Respond with two sections:\n"
        "1. **Narrative**: Your response to the player's action.\n"
        "2. **Updated Game State**: Provide the new game state in JSON format within a code block.\n\n"
        "Ensure that the **Narrative** section ends with a newline and the **Updated Game State** is properly formatted.\n\n"
        "**Example Response:**\n"
        "**Narrative**:\n"
        "Varric the Vigilant stands at the edge of a dense forest clearing, his rusty sword gleaming faintly in the sunlight. "
        "The air is thick with the scent of pine and earth. Suddenly, a Goblin Grunt emerges from the shadows, eyeing Varric warily.\n\n"
        "**Updated Game State**:\n"
        "```json\n"
        "{\n"
        '  "player": {\n'
        '    "name": "Varric the Vigilant",\n'
        '    "hp": 30,\n'
        '    "inventory": ["rusty sword", "health potion"],\n'
        '    "last_command": "start"\n'
        '  },\n'
        '  "enemies": [\n'
        '    {\n'
        '      "name": "Goblin Grunt",\n'
        '      "hp": 10,\n'
        '      "location": "forest clearing"\n'
        '    }\n'
        '  ],\n'
        '  "location": "forest clearing",\n'
        '  "description": "A dimly lit forest clearing with mossy floor and tall, ancient trees."\n'
        '}\n'
        '```'
    )

    messages = [
        {"role": "system", "content": prompt}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3.1-8b",
    )
    response = chat_completion.choices[0].message.content

    narrative, updated_game_state = parse_llm_response(response)
    print(f"Narrative: {narrative}\n")
    return updated_game_state

def main():
    client = initialize_client()

    if not os.path.exists("game_state.json"):
        shutil.copy("initial_game_state.json", "game_state.json")
        print("Game state initialized from initial_game_state.json.\n")

    game_state = load_game_state("game_state.json")

    if not game_state.get("last_command"):
        game_state = provide_initial_narrative(client, game_state)
        save_game_state("game_state.json", game_state)
        print("Game state updated successfully.\n")

    while True:
        user_input = input("Enter your action (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            print("Exiting the game. Goodbye!")
            break
        elif user_input.lower() == 'reset':
            reset_game_state("initial_game_state.json", "game_state.json")
            game_state = load_game_state("game_state.json")
            print("Game state has been reset. Starting with initial narrative...\n")
            game_state = provide_initial_narrative(client, game_state)
            save_game_state("game_state.json", game_state)
            print("Game state updated successfully.\n")
            continue

        prompt = (
            "You are a Dungeons & Dragons (D&D) assistant managing the game state. Below is the current game state:\n\n"
            f"{json.dumps(game_state, indent=2)}\n\n"
            f"Player's action: {user_input}\n\n"
            "Respond with two sections:\n"
            "1. **Narrative**: Your response to the player's action.\n"
            "2. **Updated Game State**: Provide the new game state in JSON format within a code block.\n\n"
            "Ensure that the **Narrative** section ends with a newline and the **Updated Game State** is properly formatted.\n\n"
            "**Example Response:**\n"
            "**Narrative**:\n"
            "Varric the Vigilant swings his rusty sword at the Goblin Grunt, striking it with force. The goblin recoils, losing 5 HP.\n\n"
            "**Updated Game State**:\n"
            "```json\n"
            "{\n"
            '  "player": {\n'
            '    "name": "Varric the Vigilant",\n'
            '    "hp": 30,\n'
            '    "inventory": ["rusty sword", "health potion"],\n'
            '    "last_command": "attack"\n'
            '  },\n'
            '  "enemies": [\n'
            '    {\n'
            '      "name": "Goblin Grunt",\n'
            '      "hp": 5,\n'
            '      "location": "forest clearing"\n'
            '    }\n'
            '  ],\n'
            '  "location": "forest clearing",\n'
            '  "description": "A dimly lit forest clearing with mossy floor and tall, ancient trees."\n'
            '}\n'
            '```'
        )

        messages = [
            {"role": "system", "content": prompt}
        ]

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3.1-8b",
        )
        response = chat_completion.choices[0].message.content

        narrative, updated_game_state = parse_llm_response(response)
        print(f"\nNarrative: {narrative}\n")
        game_state = updated_game_state
        save_game_state("game_state.json", game_state)
        print("Game state updated successfully.\n")

if __name__ == "__main__":
    main()