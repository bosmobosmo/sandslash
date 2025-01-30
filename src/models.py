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
    effect = TextField()
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
    back_default = TextField()
    back_female = TextField()
    back_shiny = TextField()
    back_female_shiny = TextField()
    front_default = TextField()
    front_female = TextField()
    front_shiny = TextField()
    front_shiny_female = TextField()


class PokemonStat(BaseModel):
    id = AutoField(primary_key=True)
    pokemon_id = IntegerField(index=True)
    name = TextField()
    base_state = IntegerField()
    effort = IntegerField()


class PokemonType(BaseModel):
    pokemon_id = IntegerField()
    type_id = IntegerField()

    class Meta:
        primary_key = CompositeKey("pokemon_id", "type_id")


class Type(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()


if __name__ == "__main__":
    db.connect()
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
    db.close()
