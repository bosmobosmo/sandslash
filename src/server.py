from typing import TypedDict

from flask import request
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.wrappers import Response

from models import (
    Pokemon,
    Ability,
    PokemonAbility,
    PokemonForm,
    PokemonHeldItem,
    PokemonMove,
    PokemonSprite,
    PokemonStat,
    PokemonType,
    Type,
)


class PokemonAbilityDict(TypedDict):
    name: str
    effect: str
    flavor_text: str
    is_hidden: bool
    slot: int


class PokemonDict(TypedDict):
    abilities: list[PokemonAbilityDict]
    base_experience: int
    cry: str
    forms: list[str]
    height: int
    held_items: list[str]
    id: int
    is_default: bool
    moves: list[str]
    name: str
    species: str
    sprites: dict[str, str]
    stats: list[dict[str, str | int]]
    types: list[str]
    weight: int


def serve_pokemon() -> Response:
    pokemon_id = request.args.get("id", None)
    if pokemon_id is None:
        raise BadRequest
    if int(pokemon_id) not in Pokemon:
        raise NotFound


def get_pokemon(pokemon_id: int) -> PokemonDict:
    pokemon = Pokemon[pokemon_id]
    abilities: list[PokemonAbilityDict] = []
    for pokemon_ability in PokemonAbility.select().where(
        PokemonAbility.pokemon_id == pokemon_id
    ):
        ability = Ability[pokemon_ability.ability_id]
        abilities.append(
            PokemonAbilityDict(
                name=ability.name,
                effect=ability.effect,
                flavor_text=ability.flavor_text,
                is_hidden=pokemon_ability.is_hidden,
                slot=pokemon_ability.slot,
            )
        )
    forms: list[str] = []
    for form in PokemonForm.select().where(
        PokemonForm.pokemon_id == pokemon_id
    ):
        forms.append(form.name)
    held_items: list[str] = []
    for item in PokemonHeldItem.select().where(
        PokemonHeldItem.pokemon_id == pokemon_id
    ):
        held_items.append(item.name)
    moves: list[str] = []
    for move in PokemonMove.select().where(
        PokemonMove.pokemon_id == pokemon_id
    ):
        moves.append(move.name)
    sprites = PokemonSprite[pokemon_id].__data__
    sprites.pop("pokemon_id")
    stats: list[dict[str, str | int]] = []
    for stat in PokemonStat.select().where(
        PokemonStat.pokemon_id == pokemon_id
    ):
        stats.append(
            {
                "name": stat.name,
                "base_stat": stat.base_stat,
                "effort": stat.effort,
            }
        )
    types: list[str] = []
    for pokemon_type in PokemonType.select().where(PokemonType.pokemon_id == pokemon_id):
        types.append(Type[pokemon_type.type_id].name)

    return PokemonDict(
        abilities=abilities,
        base_experience=pokemon.base_experience,
        cry=pokemon.cry,
        forms=forms,
        height=pokemon.height,
        held_items=held_items,
        id=pokemon_id,
        is_default=pokemon.is_default,
        moves=moves,
        name=pokemon.name,
        species=pokemon.species,
        sprites=sprites,
        stats=stats,
        types=types,
        weight=pokemon.weight
    )
