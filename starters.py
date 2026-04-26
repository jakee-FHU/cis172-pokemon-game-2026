from pokemon import Pokemon, Move

def make_starters():
    # moves
    vine_whip = Move("Vine Whip", "Grass", 8, 100)
    tackle = Move("Tackle", "Normal", 5, 100)
    ember = Move("Ember", "Fire", 9, 100)
    scratch = Move("Scratch", "Normal", 6, 100)
    water_gun = Move("Water Gun", "Water", 9, 100)

    # starter Pokemon
    starters = [
        Pokemon("Bulbasaur", 110, 18, "Grass", "Fire"),
        Pokemon("Charmander", 95, 20, "Fire", "Water"),
        Pokemon("Squirtle", 105, 19, "Water", "Electric")
    ]

    starters[0].moves = [vine_whip, tackle]
    starters[1].moves = [ember, scratch]
    starters[2].moves = [water_gun, tackle]

    return starters

def make_pokemon(species):
    vine_whip = Move("Vine Whip", "Grass", 8, 100)
    tackle = Move("Tackle", "Normal", 5, 100)
    ember = Move("Ember", "Fire", 9, 100)
    scratch = Move("Scratch", "Normal", 6, 100)
    water_gun = Move("Water Gun", "Water", 9, 100)

    if species == "Bulbasaur":
        bulbasaur = Pokemon("Bulbasaur", 110, 18, "Grass", "Fire")
        bulbasaur.moves = [vine_whip, tackle]
        return bulbasaur
    elif species == "Charmander":
        charmander = Pokemon("Charmander", 95, 20, "Fire", "Water")
        charmander.moves = [ember, scratch]
        return charmander
    elif species == "Squirtle":
        squirtle = Pokemon("Squirtle", 105, 19, "Water", "Electric")
        squirtle.moves = [water_gun, tackle]
        return squirtle

def choose_starter(starters):
    print("\n--- CHOOSE YOUR STARTER ---")
    for i, pokemon in enumerate(starters):
        # [num]. [Pokemon species] ([Pokemon element type])
        print(f"{i+1}. {pokemon.species} ({pokemon.elem_type})")

    # take input and subtract 1 to match zero-index list of Pokemon:
    choice = int(input("\n> ")) - 1
    selected = starters[choice]
    
    # let player rename their Pokemon:
    print(f"\nYou chose {selected.species}!\nEnter a nickname for your {selected.species} (or press Enter to keep default name):")
    new_name = input(f"\n> ")

    if new_name:
        selected.name = new_name
        print(f"\nYour {selected.species} has been nicknamed {selected.name}!")

    # remove selection from the list of starters so rival can't choose it:
    starters.pop(choice)
    return selected