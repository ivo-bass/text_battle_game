import random

from classes.game import Person, check_for_winner
from classes.magic import Spell
from classes.inventory import Item
from classes.colors import Colors


# Create black magic
fire = Spell("Fire - 300 HP", 15, 300, "black")
thunder = Spell("Thunder - 400 HP", 20, 400, "black")
blizzard = Spell("Blizzard - 600 HP", 30, 600, "black")
meteor = Spell("Meteor - 1100 HP", 50, 1100, "black")
quake = Spell("Quake - 2200 HP", 90, 2200, "black")

# Create white magic
heal = Spell("Heal - 600 HP", 30, 600, "white")
cure = Spell("Cure - 1500 HP", 75, 1500, "white")


# Create some items
potion = Item("Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP and MP of ONE party member", 9999)
hi_elixer = Item("Mega Elixer", "elixer", "Fully restores HP and MP of ALL party members", 9999)
grenade = Item("Grenade", "attack", "Deals 300 damage to all enemies", 300)
nuclear_bomb = Item("Nuclear Bomb", "attack", "Deals 1000 damage to all enemies", 1000)

# Assign spells and items to players
player_spells = [fire, thunder, blizzard, meteor, quake, heal, cure]
player_items = [{"item": potion, "quantity": 5},
                {"item": super_potion, "quantity": 3},
                {"item": elixer, "quantity": 1},
                {"item": hi_elixer, "quantity": 1},
                {"item": grenade, "quantity": 3},
                {"item": nuclear_bomb, "quantity": 1}]

# Assign spells to enemies. No items for now.
enemy_spells = [fire, meteor, heal]
enemy_items = []

# Create characters
player1 = Person("Joe-1 ", 2600, 120, 220, 250, player_spells, player_items)
player2 = Person("Joe-2 ", 3000, 90, 240, 250, player_spells, player_items)
player3 = Person("Joe-3 ", 2200, 140, 200, 250, player_spells, player_items)
players = [player1, player2, player3]

enemy1 = Person("Magnus", 3000, 300, 400, 200, enemy_spells, enemy_items)
enemy2 = Person("BOSS  ", 12000, 100, 600, 500, enemy_spells, enemy_items)
enemy3 = Person("Carlos", 4000, 300, 300, 300, enemy_spells, enemy_items)
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(Colors.WARNING +
      "This is a text battle game with 3 players and 3 enemies. Players can attack enemies and heal themselves.\n"
      "Each party member has different stats as Hit Points, Magic Points, Attack Power etc.\n"
      "In order to be more interesting some stats are not revealed.\n"
      "Enemies can also attack, spell and heal and nothing but their HP is known.\n"
      "The user should build some strategy for the game to avoid losing." +
      Colors.ENDC)
print(Colors.FAIL + Colors.BOLD + Colors.UNDERLINE + "\nENEMIES ATTACK!" + Colors.ENDC)

while running:
    # Display stats of all party members at the start of each loop
    print(Colors.BOLD + Colors.FAIL +
          "_________________________________________________________________________\n" + Colors.ENDC)
    print(Colors.OKGREEN + "PLAYER                HP                                      MP" + Colors.ENDC)
    for player in players:
        player.get_stats()
    print("\n")

    print(Colors.FAIL + "ENEMY                 HP" + Colors.ENDC)
    for enemy in enemies:
        enemy.get_enemy_stats()

    # Players attack phase
    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        if choice not in ("1", "2", "3"):
            print(Colors.WARNING + "You missed your turn... Be careful with numbers." + Colors.ENDC)
            continue
        else:
            index = int(choice) - 1

            # Player choice == ATTACK
            if index == 0:
                enemy = player.choose_target(enemies)
                if enemy is False:
                    continue
                else:
                    dmg = player.generate_dmg()
                    enemies[enemy].take_dmg(dmg)
                    print(Colors.OKGREEN + "You attacked", enemies[enemy].name.replace(" ", ""), "for", dmg,
                          "points of damage." + Colors.ENDC)

                    # Check if the target has died
                    if enemies[enemy].get_hp() <= 0:
                        print(Colors.BOLD + Colors.OKGREEN + enemies[enemy].name.replace(" ", "") +
                              " has died!" + Colors.ENDC)
                        del enemies[enemy]

            # Player choice == MAGIC
            elif index == 1:
                player.choose_magic()
                choice = input("    Choose magic: ")

                if choice not in ("1", "2", "3", "4", "5", "6", "7"):
                    print(Colors.WARNING + "You missed your turn... Be careful with numbers." + Colors.ENDC)
                    continue
                else:
                    magic_choice = int(choice) - 1
                    spell = player.magic[magic_choice]
                    magic_dmg = spell.generate_dmg()

                    current_mp = player.get_mp()

                    # Check if the player has enough magic points to use the spell
                    if spell.cost > current_mp:
                        print(Colors.FAIL + "\nNot enough MP!\nYou missed your turn!" + Colors.ENDC)
                        continue

                    player.reduce_mp(spell.cost)

                    # White magic heals the player
                    if spell.type == "white":
                        player.heal(magic_dmg)
                        print(Colors.OKBLUE + '"' + spell.name + '"' + " heals for", str(magic_dmg), "HP." + Colors.ENDC)

                    # Black magic deals damage to enemy
                    elif spell.type == "black":
                        enemy = player.choose_target(enemies)
                        if enemy is False:
                            continue
                        else:
                            enemies[enemy].take_dmg(magic_dmg)
                            print(Colors.OKBLUE + '"' + spell.name + '"' + " deals", str(magic_dmg),
                                  "points of damage to " + enemies[enemy].name.replace(" ", "") + "!" + Colors.ENDC)

                            # Check if enemy has died
                            if enemies[enemy].get_hp() == 0:
                                print(Colors.BOLD + Colors.OKGREEN + enemies[enemy].name.replace(" ", "") +
                                      " has died!" + Colors.ENDC)
                                del enemies[enemy]

            # Player choice == ITEM
            elif index == 2:
                player.choose_item()
                choice = input("    Choose item: ")

                if choice not in ("1", "2", "3", "4", "5", "6"):
                    print(Colors.WARNING + "You missed your turn... Be careful with numbers." + Colors.ENDC)
                    continue
                else:
                    item_choice = int(choice) - 1
                    item = player.items[item_choice]["item"]

                    # Check if the player has enough of the chosen item
                    if player.items[item_choice]["quantity"] == 0:
                        print(Colors.WARNING + "\nNone left...\nYou missed your turn!" + Colors.ENDC)
                        continue
                    player.items[item_choice]["quantity"] -= 1

                    # The "potion" type item heals current player with it's property number of hit points
                    if item.type == "potion":
                        player.heal(item.prop)
                        print(Colors.OKBLUE + item.name + " heals for", str(item.prop), "HP." + Colors.ENDC)

                    # Elixer returns full HP and MP
                    elif item.type == "elixer":
                        # Loop through all players to refill all of theirs HP and MP with the Mega Elixer
                        if item.name == "Mega Elixer":
                            for i in players:
                                i.hp = i.max_hp
                                i.mp = i.max_mp
                        else:
                            player.hp = player.max_hp
                            player.mp = player.max_mp
                        print(Colors.OKBLUE + item.name, item.description + Colors.ENDC)

                    elif item.type == "attack":
                        # Attacking all enemies at once!
                        enemies_left_count = len(enemies)
                        e = 0
                        while e < enemies_left_count:
                            enemies[e].take_dmg(item.prop)
                            print(Colors.OKBLUE + item.name + " deals", str(item.prop),
                                  "points of damage to " + enemies[e].name.replace(" ", "") + "!" + Colors.ENDC)

                        # Check if some of the enemies has died
                            if enemies_left_count > 0 and enemies[e].get_hp() == 0:
                                print(Colors.BOLD + Colors.OKGREEN + enemies[e].name.replace(" ", "") +
                                      " has died!" + Colors.ENDC)
                                enemies_left_count -= 1
                                del enemies[e]

                            e += 1

        # Check for winner
        running = check_for_winner(players, enemies)
        if running is False:
            break

    # Enemies attack phase
    if running is False:
        break
    print(Colors.BOLD + Colors.FAIL + Colors.UNDERLINE + "\nENEMIES ATTACK!" + Colors.ENDC)
    print(Colors.BOLD + Colors.FAIL +
          "_________________________________________________________________________" + Colors.ENDC)
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        # If enemy chose to attack
        if enemy_choice == 0:
            target = random.randrange(len(players))
            enemy_dmg = enemy.generate_dmg()
            players[target].take_dmg(enemy_dmg)
            print(Colors.FAIL + enemy.name.replace(" ", "") + " attacks " +
                  players[target].name.replace(" ", "") + " for", str(enemy_dmg) + "!" + Colors.ENDC)

            if players[target].get_hp() == 0:
                print(Colors.FAIL + Colors.BOLD + players[target].name.replace(" ", "") + " has died!" + Colors.ENDC)
                del players[target]

            running = check_for_winner(players, enemies)
            if running is False:
                break

        # If enemy chose magic
        elif enemy_choice == 1:
            target = random.randrange(len(players))
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(Colors.OKBLUE + spell.name + " heals", enemy.name.replace(" ", ""), "for",
                      str(magic_dmg), "HP." + Colors.ENDC)
            elif spell.type == "black":
                players[target].take_dmg(magic_dmg)
                print(Colors.OKBLUE + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + players[target].name.replace(" ", "") + "!" + Colors.ENDC)

            if players[target].get_hp() == 0:
                print(Colors.FAIL + Colors.BOLD + players[target].name.replace(" ", "") + " has died!" + Colors.ENDC)
                del players[target]
                running = check_for_winner(players, enemies)
                if running is False:
                    break
        else:
            pass

input("\nPress ENTER to exit")
