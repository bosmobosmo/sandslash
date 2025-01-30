# Sandslash

## How it works
Fetch Pokemon data from [PokeAPI](http://pokeapi.co) and store them in a local SQLite database.

## Design considerations

### Why use SQLite
Because it's fast and easy.

### Why some data are omitted
To reduce the number of tables. Some metadata can be omitted without compromising the description of the Pokemons.
