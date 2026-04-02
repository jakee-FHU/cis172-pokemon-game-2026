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
        base = self.power + attacker.attack_power

        # element effectiveness system:
        # -------------------
        
        return int(base)