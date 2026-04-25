import random

class Pokemon():
    def __init__(self, species, max_health, attack_power, elem_type, elem_weakness):
        # pokemon's name (input by player, species by default):
        self.name = species
        # pokemon type (i.e. Pikachu):
        self.species = species
        # maximum health points:
        self.max_health = max_health
        # current health points:
        self.health = max_health
        # base attack strength:
        self.attack_power = attack_power
        # element type:
        self.elem_type = elem_type
        # elemental weakness:
        self.elem_weakness = elem_weakness
        # composition list of available moves:
        self.moves = []
        # sprite:
        self.sprite = species.lower()

    # performs selected move and deals damage to opponent based on attack_power and elem_type, and opponent's elem_weakness:
    def attack(self, move, opponent):
        damage = move.calc_damage(self, opponent)
        opponent.damage(damage)

    # reduce health when taking a hit based on elem_weakness and opponent's attack_power and elem_type:
    def damage(self, amount):
        self.health -= amount

        if self.health < 0:
            self.health = 0
        
        print(f"{self.name} took {amount} damage! ({self.health}/{self.max_health} HP)")

        if self.health == 0:
            self.faint()

    # handle Pokemon fainting (lost all health):
    def faint(self):
        print(f"\n{self.name} fainted!")


class Move():
    def __init__(self, name, elem_type, power, accuracy):
        # move name:
        self.name = name
        # move element type:
        self.elem_type = elem_type
        # base move attack power:
        self.power = power
        # base move accuracy:
        self.accuracy = accuracy
    
    # calculates damage of move based on move attributes, attacker's attack_power and elem_type, and opponent's elem_weakness:
    def calc_damage(self, attacker, opponent):
        base_dmg = self.power
        effectiveness = 1.0

        # elemental advantage
        if self.elem_type == "Fire" and opponent.elem_type == "Grass":
            effectiveness = 1.25
        elif self.elem_type == "Grass" and opponent.elem_type == "Water":
            effectiveness = 1.25
        elif self.elem_type == "Water" and opponent.elem_type == "Fire":
            effectiveness = 1.25
                                                                            ### Numbers are pretty extreme but just wanted to get a system set up ###
        # weak cases
        elif self.elem_type == "Fire" and opponent.elem_type == "Water":
            effectiveness = 0.8
        elif self.elem_type == "Grass" and opponent.elem_type == "Fire":
            effectiveness = 0.8
        elif self.elem_type == "Water" and opponent.elem_type == "Grass":
            effectiveness = 0.8

        #randomness 
        variation = random.uniform(0.9, 1.1) #+- 15% dmg, could alter this

        # final damage
        dmg = base_dmg * effectiveness * variation

        return int(dmg)