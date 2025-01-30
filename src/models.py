from peewee import AutoField, BooleanField, CompositeKey, IntegerField, Model, TextField


class Ability(Model):
    id = IntegerField(primary_key=True)
    name = TextField()
    effect = TextField()
    flavor_text = TextField()


class Pokemon(Model):
    id = IntegerField(primary_key=True)
    name = TextField()
    base_experience = IntegerField()
    height = IntegerField()
    weight = IntegerField()
    cry = TextField()  # only use latest
    species = TextField()
    order = IntegerField()
    is_default = BooleanField()


class PokemonAbility(Model):
    pokemon_id = IntegerField()
    ability_id = IntegerField()
    is_hidden = BooleanField()
    slot = IntegerField()
    is_past = BooleanField(default=False)
    generation = TextField(null=True)

    class Meta:
        primary_key = CompositeKey("pokemon_id", "ability_id")


class PokemonForm(Model):
    id = AutoField(primary_key=True)
    name = TextField()
    pokemon_id = IntegerField(index=True)


class PokemonFormType(Model):
    form_id = IntegerField()
    type_id = IntegerField()

    class Meta:
        primary_key = CompositeKey("form_id", "type_id")


class PokemonHeldItem(Model):
    id = AutoField(primary_key=True)
    pokemon_id = IntegerField()
    name = TextField()


class PokemonHeldItemVersionDetail(Model):
    id = AutoField(primary_key=True)
    pokemon_held_item_id = IntegerField(index=True)
    rarity = IntegerField()
    name = TextField()


class PokemonMove(Model):
    id = AutoField(primary_key=True)
    pokemon_id = IntegerField(index=True)
    name = TextField()


class PokemonMoveVersionGroupDetail(Model):
    id = AutoField(primary_key=True)
    pokemon_move_id = IntegerField(index=True)
    level_learned_at = IntegerField()
    move_learn_method = TextField()
    version_group = TextField()


class PokemonSprite(Model):
    back_default = TextField()
    back_female = TextField()
    back_shiny = TextField()
    back_female_shiny = TextField()
    front_default = TextField()
    front_female = TextField()
    front_shiny = TextField()
    front_shiny_female = TextField()


class PokemonStat(Model):
    id = AutoField(primary_key=True)
    pokemon_id = IntegerField(index=True)
    name = TextField()
    base_state = IntegerField()
    effort = IntegerField()


class PokemonType(Model):
    pokemon_id = IntegerField()
    type_id = IntegerField()
    is_past = BooleanField(default=False)
    generation = TextField(null=True)

    class Meta:
        primary_key = CompositeKey("pokemon_id", "type_id")


class Type(Model):
    id = IntegerField(primary_key=True)
    name = TextField()
