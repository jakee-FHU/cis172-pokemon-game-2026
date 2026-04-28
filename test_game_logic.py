import pytest
from starters import make_pokemon
from trainer import Trainer, Rival

### Fixtures ###
@pytest.fixture
def bulbasaur():
    return make_pokemon("Bulbasaur")

@pytest.fixture
def charmander():
    return make_pokemon("Charmander")

@pytest.fixture
def squirtle():
    return make_pokemon("Squirtle")


### Simple logic tests ###
def test_make_pokemon_species(bulbasaur, charmander, squirtle):
    assert bulbasaur.species == "Bulbasaur"
    assert charmander.species == "Charmander"
    assert squirtle.species == "Squirtle"

def test_damage_reduces_health(bulbasaur):
    bulbasaur.damage(10)
    assert bulbasaur.health == bulbasaur.max_health - 10

def test_new_pokemon_starts_full_health(charmander):
    assert charmander.max_health == charmander.health

def test_pokemon_has_two_moves(squirtle):
    assert len(squirtle.moves) == 2

def test_rival_choose_move_returns_move(bulbasaur):
    rival = Rival("Opponent")
    rival.active_pokemon = bulbasaur

    move = rival.choose_move()

    assert move in rival.active_pokemon.moves

### AI Assisted ###
def test_make_pokemon_creates_fresh_instances():
    p1 = make_pokemon("Bulbasaur")
    p2 = make_pokemon("Bulbasaur")

    assert p1 is not p2

    p1.damage(20)

    assert p1.health != p2.health
    assert p2.health == p2.max_health

def test_damage_does_not_go_below_zero(charmander):
    charmander.damage(999)
    assert charmander.health == 0

def test_super_effective_move_does_more_than_base_range(charmander, bulbasaur):

    ember = charmander.moves[0]  # Fire move

    damage = ember.calc_damage(charmander, bulbasaur)

    assert damage >= ember.power

def test_trainer_has_usable_pokemon_when_one_alive(bulbasaur, charmander):
    trainer = Trainer("Player")

    p1 = bulbasaur
    p2 = charmander

    p1.health = 0
    p2.health = 10

    trainer.party = [p1, p2]

    assert trainer.has_usable_pokemon() is True

def test_trainer_has_usable_pokemon_returns_false_when_all_fainted(bulbasaur, squirtle):
    trainer = Trainer("Player")

    p1 = bulbasaur
    p2 = squirtle

    p1.health = 0
    p2.health = 0

    trainer.party = [p1, p2]

    assert trainer.has_usable_pokemon() is False