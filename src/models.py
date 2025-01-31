from peewee import (
    AutoField,
    BooleanField,
    CompositeKey,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

db = SqliteDatabase("poke.db")


class BaseModel(Model):
    class Meta:
        database = db


class Ability(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    effect = TextField(null=True)
    flavor_text = TextField()


class Pokemon(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    base_experience = IntegerField()
    height = IntegerField()
    weight = IntegerField()
    cry = TextField()  # only use latest
    species = TextField()
    order = IntegerField()
    is_default = BooleanField()


class PokemonAbility(BaseModel):
    pokemon_id = IntegerField()
    ability_id = IntegerField()
    is_hidden = BooleanField()
    slot = IntegerField()

    class Meta:
        primary_key = CompositeKey("pokemon_id", "ability_id")


class PokemonForm(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField()
    pokemon_id = IntegerField(index=True)


class PokemonHeldItem(BaseModel):
    id = AutoField(primary_key=True)
    pokemon_id = IntegerField()
    name = TextField()


class PokemonMove(BaseModel):
    id = AutoField(primary_key=True)
    pokemon_id = IntegerField(index=True)
    name = TextField()


class PokemonSprite(BaseModel):
    pokemon_id = IntegerField(primary_key=True)
    back_default = TextField(null=True)
    back_female = TextField(null=True)
    back_shiny = TextField(null=True)
    back_female_shiny = TextField(null=True)
    front_default = TextField(null=True)
    front_female = TextField(null=True)
    front_shiny = TextField(null=True)
    front_shiny_female = TextField(null=True)


class PokemonStat(BaseModel):
    id = AutoField(primary_key=True)
    pokemon_id = IntegerField(index=True)
    name = TextField()
    base_stat = IntegerField()
    effort = IntegerField()


class PokemonType(BaseModel):
    pokemon_id = IntegerField()
    type_id = IntegerField()

    class Meta:
        primary_key = CompositeKey("pokemon_id", "type_id")


class Type(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()


def create_tables() -> None:
    db.create_tables(
        [
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
        ]
    )
