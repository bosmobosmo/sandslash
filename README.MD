# Sandslash

## Requirements
- Python ^3.12
- [Poetry](https://python-poetry.org/)

## Commands
The commands are called using `python src/main.py <command>`.

`scrape`: Scrape pokemon data and store them into a local database. This will do fetches sequentially starting from id stored in `last_scrape_attempt.txt` or the env var `START_ID`, whichever is bigger. Any pokemons already scraped will be skipped.

`serve`: Starts a Flask server that returns pokemon data. The route is `/pokemon?id=<pokemon-id>`.

`init`: Initialize the database to store pokemon data.

## How it works
Fetch pokemon data from [PokeAPI](http://pokeapi.co) and store them in a local SQLite database. Also fetch and store the pokemon's abilities but not other details like items or moves.

Scrape might raise an error when PokeAPI returns an unexpected null value. This is because the scraper is not yet tested against **all** existing pokemons. The fix is to alter the table to allow null value.

The server queries all relevant data of a pokemon and return it as a json file. Quite similar with what PokeAPI returns except that abilites are expanded further and URLs to other details are omitted.

## Design considerations

### Why use SQLite
Because it's fast and easy.

### Why some data are omitted
To reduce the number of tables. Some metadata can be omitted without compromising the description of the pokemon. The project's goal is to showcase the ability to store data efficiently, not to make yet another highly detailed pokemon database.

### Why Sandslash
Because it scrapes.
