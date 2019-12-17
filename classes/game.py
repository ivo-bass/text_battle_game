import random
from classes.colors import Colors
from classes.magic import Spell


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.actions = ["ATTACK (Choose a target and hit the enemy with a bat)",
                        "MAGIC (Choose a magic spell, then select the target)",
                        "ITEMS (Choose an item from your inventory)"]
        self.items = items
        self.name = name

    def generate_dmg(self):
        return random.randrange(self.atkl, self.atkh)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + "    " + Colors.BOLD + self.name + Colors.ENDC)
        print(Colors.OKBLUE + Colors.BOLD + "    ACTIONS:" + Colors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + Colors.OKBLUE + Colors.BOLD + "    MAGIC:" + Colors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + Colors.OKGREEN + Colors.BOLD + "    ITEMS:" + Colors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name + ":", item["item"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + Colors.FAIL + Colors.BOLD + "    TARGET:" + Colors.ENDC)
        if len(enemies) == 1:
            print("    Only 1 enemy still alive!")
            return 0
        else:
            for enemy in enemies:
                if enemy.get_hp() != 0:
                    print("        " + str(i) + ".", enemy.name)
                    i += 1
            choice = input("    Choose target: ")
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # To be debugged! Choice must be in the count of enemies alive.
            if choice not in ("1", "2", "3"):
                print(Colors.WARNING + "You missed your turn... Be careful with writing numbers." + Colors.ENDC)
                return False
            else:
                index = int(choice) - 1
                return index

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_dmg()
        return spell, magic_dmg

    def get_enemy_stats(self):
        hp_bar = ""
        hp_ticks = self.hp / self.max_hp * 100 / 2
        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1
        while len(hp_bar) < 50:
            hp_bar += " "
        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""
        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string
        print("                      __________________________________________________")
        print(Colors.BOLD + self.name + "   " + current_hp + " |" + Colors.FAIL +
              hp_bar + Colors.ENDC + Colors.BOLD + "|" + Colors.ENDC)

    def get_stats(self):
        hp_bar = ""
        hp_ticks = self.hp / self.max_hp * 100 / 4
        mp_bar = ""
        mp_ticks = self.mp / self.max_mp * 100 / 10
        while hp_ticks > 0:
            hp_bar += "█"
            hp_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "
        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += " "
        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""
        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string
        mp_string = str(self.mp) + "/" + str(self.max_mp)
        current_mp = ""
        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)
            while decreased > 0:
                current_mp += " "
                decreased -= 1
            current_mp += mp_string
        else:
            current_mp = mp_string
        print("                      _________________________               __________")
        print(Colors.BOLD + self.name + "     " + current_hp + " |" + Colors.OKGREEN +
              hp_bar + Colors.ENDC + Colors.BOLD +
              "|     " + current_mp + " |" + Colors.OKBLUE +
              mp_bar + Colors.ENDC + Colors.BOLD + "|" + Colors.ENDC)


def check_for_winner(players, enemies):
    if len(players) == 0:
        print(Colors.BOLD + Colors.WARNING + "\n     ____GAME OVER____\n    ____YOU LOST!!!____" + Colors.ENDC)
        running = False
    elif len(enemies) == 0:
        print(Colors.BOLD + Colors.WARNING + "\n    ALL ENEMIES DEFEATED!\n     ***** YOU WIN *****" + Colors.ENDC)
        running = False
    else:
        running = True
    return running
