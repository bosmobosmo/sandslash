import argparse
from pathlib import Path
import os

from models import Pokemon
from scraper import scrape

START_ID = os.environ.get("START_ID", 0)


def scrape_continuously() -> None:
    pokemon_id = int(START_ID)
    # Hack because setting env var in Powershell is convoluted
    last_attempt_note = Path(__file__).parent.joinpath(
        "last_scrape_attempt.txt"
    )
    with last_attempt_note.open() as f:
        last_attempted_id = f.read().strip()
        if last_attempted_id.isnumeric():
            pokemon_id = max(pokemon_id, int(last_attempted_id))

    while True:
        try:
            # Skip stored Pokemons
            while pokemon_id in Pokemon:
                pokemon_id += 1
                # id jumps from 1025 to 10001
                if pokemon_id == 1026:
                    pokemon_id = 10001
            scrape(str(pokemon_id))
        finally:
            with last_attempt_note.open("w") as f:
                f.write(str(pokemon_id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    args = parser.parse_args()
    match args.command:
        case "scrape":
            scrape_continuously()
        case _:
            print(f"Command {args.command} not found")
