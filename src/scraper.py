import requests

from models import (
    db,
    Ability,
    Pokemon,
    PokemonAbility,
    PokemonForm,
    PokemonHeldItem,
    PokemonMove,
    PokemonSprite,
    PokemonStat,
    PokemonType,
    Type,
)

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"


def scrape(pokemon_id=str):
    # Fetch from API
    pokemon_response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}")
    pokemon_response.raise_for_status()
    pokemon_json = pokemon_response.json()

    # Create objects
    pokemon = Pokemon(**pokemon_json)
    pokemon.cry = pokemon_json["cries"]["latest"]
    pokemon.species = pokemon_json["species"]["name"]
    pokemon_abilities: list[PokemonAbility] = []
    new_abilities: list[Ability] = []
    pokemon_forms: list[PokemonForm] = []
    pokemon_moves: list[PokemonMove] = []
    pokemon_sprite = PokemonSprite(
        pokemon_id=pokemon_id, **pokemon_json["sprites"]
    )
    pokemon_stats: list[PokemonStat] = []
    pokemon_types: list[PokemonType] = []
    new_types: list[Type] = []
    pokemon_held_items: list[PokemonHeldItem] = []
    for ability in pokemon_json["abilities"]:
        ability_id = ability["ability"]["url"].split("/")[-2]
        if int(ability_id) not in Ability:
            ability_response = requests.get(ability["ability"]["url"])
            ability_response.raise_for_status()
            ability_json = ability_response.json()
            new_ability = Ability(
                id=int(ability_id),
                name=ability_json["name"],
            )
            for effect in ability_json["effect_entries"]:
                if effect["language"]["name"] == "en":
                    new_ability.effect = effect["effect"]
                    break
            for flavor_text in ability_json["flavor_text_entries"]:
                if flavor_text["language"]["name"] == "en":
                    new_ability.flavor_text = flavor_text["flavor_text"]
                    break
            new_abilities.append(new_ability)
        pokemon_ability = PokemonAbility(**ability)
        pokemon_ability.pokemon_id = pokemon_id
        pokemon_ability.ability_id = ability_id
        pokemon_abilities.append(pokemon_ability)
    for form in pokemon_json["forms"]:
        pokemon_forms.append(
            PokemonForm(pokemon_id=pokemon_id, name=form["name"])
        )
    for move in pokemon_json["moves"]:
        pokemon_moves.append(
            PokemonMove(pokemon_id=pokemon_id, name=move["move"]["name"])
        )
    for stat in pokemon_json["stats"]:
        pokemon_stats.append(
            PokemonStat(
                pokemon_id=pokemon_id, name=stat["stat"]["name"], **stat
            )
        )
    for type in pokemon_json["types"]:
        type_id = type["type"]["url"].split("/")[-2]
        if int(type_id) not in Type:
            new_types.append(Type(id=int(type_id), name=type["type"]["name"]))
        pokemon_types.append(
            PokemonType(pokemon_id=pokemon_id, type_id=int(type_id))
        )
    for held_item in pokemon_json["held_items"]:
        pokemon_held_items.append(
            PokemonHeldItem(
                pokemon_id=pokemon_id, name=held_item["item"]["name"]
            )
        )

    # Store to db in a single transaction
    with db.atomic() as tx:
        try:
            pokemon.save(force_insert=True)
            pokemon_sprite.save(force_insert=True)
            for attributes in [
                pokemon_abilities,
                new_abilities,
                pokemon_forms,
                pokemon_moves,
                pokemon_types,
                new_types,
                pokemon_stats,
                pokemon_held_items,
            ]:
                for attribute in attributes:
                    attribute.save(force_insert=True)
        except:
            tx.rollback()
            raise


if __name__ == "__main__":
    scrape("1")
