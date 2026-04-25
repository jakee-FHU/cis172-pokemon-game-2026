import random

class Trainer:
    def __init__(self, name='Player'):
        # trainer name (input by player, defaults to 'Player'):
        self.name = name
        # list of Pokemon in trainer's party (aggregation):
        self.party = []
        # number of healing items in trainer's bag (aggregation):
        self.potions = 10
        # tracks the currently active Pokemon:
        self.active_pokemon = None
    
    # choose a move to perform:
    def choose_move(self):
        print("\nChoose a move:")
        for i, move in enumerate(self.active_pokemon.moves):
            # [num]. [Pokemon name]
            print(f"{i+1}. {move.name}")

        # take input and subtract 1 to match zero-index list of Pokemon:
        choice = int(input("\n> ")) - 1
        return self.active_pokemon.moves[choice]

    # switch between Pokemon during battle:
    def switch_pokemon(self):
        for i, pokemon in enumerate(self.party):
            # if fainted, specify beside name:
            if pokemon.health == 0:
                print(f"{i+1}. {pokemon.name} (Fainted)")
            else:
                print(f"{i+1}. {pokemon.name}")

        # take input and subtract 1 to match zero-index list of Pokemon:
        choice = int(input("\n> ")) - 1
        selected = self.party[choice]

        if selected.health == 0:
            print(f"{selected.name} has fainted!")
        else:
            self.active_pokemon = selected
            print(f"Go, {selected.name}!")
            return
        
    # heal during battle:
    def use_potion(self, pokemon):
        self.potions -= 1
        default_heal_amount = 20

        missing_health = pokemon.max_health - pokemon.health
        heal_amount = min(default_heal_amount, missing_health)
        pokemon.health += heal_amount
        return heal_amount

    def has_usable_pokemon(self):
        for pokemon in self.party:
            if pokemon.health > 0:
                return True
        return False
    
    def handle_pokemon_faint(self):
        if self.active_pokemon.health == 0 and self.has_usable_pokemon():
            print("\nYour active Pokemon fainted! Choose a new Pokemon:")
            self.switch_pokemon()


class Rival(Trainer):
    def __init__(self, name='Rival'):
        super().__init__(name)

    # override to choose move at random:
    def choose_move(self):
        return random.choice(self.active_pokemon.moves)

    # override to switch to next Pokemon when current one faints:
    def switch_pokemon(self):
        for pokemon in self.party:
            if pokemon.health > 0:
                self.active_pokemon = pokemon
                print(f"\n{self.name} sent out {pokemon.name}!")
                return
            
    def handle_pokemon_faint(self):
        if self.active_pokemon.health == 0 and self.has_usable_pokemon():
            self.switch_pokemon()