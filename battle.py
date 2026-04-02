class Battle:
    def __init__(self, player, rival):
        # participating player trainer:
        self.player = player
        # participating rival trainer:
        self.rival = rival

    # begin battle loop:
    def start_battle(self):
        print("\n--- START OF BATTLE ---")

        # keep looping until a winner is declared:
        while True:
            self.show_status()

            self.player_turn()
            self.faint_check()
            if self.win_check():
                print("\n--- END OF BATTLE ---")
                break

            self.rival_turn()
            self.faint_check()
            if self.win_check():
                print("\n--- END OF BATTLE ---")
                break

    # handle player turn:
    def player_turn(self):
        move = self.player.choose_move()
        print(f"\n{self.player.active_pokemon.name} used {move.name}!")
        self.player.active_pokemon.attack(move, self.rival.active_pokemon)

    # handle rival turn:
    def rival_turn(self):
        move = self.rival.choose_move()
        print(f"\n{self.rival.active_pokemon.name} used {move.name}!")
        self.rival.active_pokemon.attack(move, self.player.active_pokemon)

    # display current status of player and rival Pokemon after each turn:
    def show_status(self):
        print("\n--- STATUS ---")
        print(f"{self.player.name.upper()}:\t {self.player.active_pokemon.name} ({self.player.active_pokemon.health}/{self.player.active_pokemon.max_health} HP)")
        print(f"{self.rival.name.upper()}:\t {self.rival.active_pokemon.name} ({self.rival.active_pokemon.health}/{self.rival.active_pokemon.max_health} HP)")

    def faint_check(self):
        self.player.handle_pokemon_faint()
        self.rival.handle_pokemon_faint()

    # check if either trainer's Pokemon party has fainted:
    def win_check(self):
        # player lost:
        if not self.player.has_usable_pokemon():
            print("\nAll your Pokemon have fainted! You lose!")
            return True

        # player won:
        if not self.rival.has_usable_pokemon():
            print("\nAll rival Pokemon have fainted! You win!")
            return True

        return False