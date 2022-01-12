import json
import random
import numpy

class gbf_rolls:
    R_rate = 0.82
    SR_rate = 0.15
    SSR_rate = 0.03
    ten_SR_rate = 0.97

    SSR_individual_rate = 0.008
    SSR_rate_up = 0.350
    SSR_weapons_rate = 0.80
    SSR_summons_rate = 0.2

    SR_character_weapons_rate = 0.05
    SR_non_character_weapons_rate = 0.06
    SR_weapons_rate = SR_character_weapons_rate + SR_non_character_weapons_rate
    SR_weapons_rate = 0.73
    SR_summons_rate = 0.27

    R_character_weapon_rate = 0.206
    R_non_character_weapon_rate = 0.692
    #R_weapons_rate = R_character_weapon_rate + R_non_character_weapon_rate 
    R_weapons_rate = 0.66
    R_summons_rate = 0.33

    reg_pull_weight = [R_rate, SR_rate, SSR_rate]
    ten_pull_weight = [0, ten_SR_rate, SSR_rate] 

    R_weapons = []
    SR_weapons = []
    SSR_weapons = []

    R_summons = []
    SR_summons = []
    SSR_summons = []

    def __init__(self):
        # self.__setup_weapons()
        self.__setup_new_weapons()
        self.__setup_summons()
        print("Successfully setup gacha db")

    
    def pull(self, weight=reg_pull_weight):
        pull_rarity = ['r', 'sr', 'ssr']
        result = random.choices(pull_rarity, weight, k=1)[0]
        return self.__pick_unit(result)

    def ten_pull(self):
        pulls = []
        for i in range(9):
            pulls.append(self.pull())

        #last roll is guarantee SR/SSR
        pulls.append(self.pull(self.ten_pull_weight))

        return pulls

    def __setup_summons(self):
        with open ("src/db/updated_draw_summons.json") as summonfile:
            all_summons = json.load(summonfile)
            for summon in all_summons:
                if summon['rarity'] == 'r':
                    self.R_summons.append(summon)
                elif summon['rarity'] == 'sr':
                    self.SR_summons.append(summon)
                elif summon['rarity'] == 'ssr':
                    self.SSR_summons.append(summon)


    def __setup_weapons(self):
        with open ("src/db/premium_draw_weapons.json") as weaponfile:
            all_weapons = json.load(weaponfile)
            for weapon in all_weapons:
                if weapon[1] == "r":
                    self.R_weapons.append(weapon)
                elif weapon[1] == 'sr':
                    self.SR_weapons.append(weapon)
                elif weapon[1] == 'ssr':
                    self.SSR_weapons.append(weapon)
    
    def __setup_new_weapons(self):
        with open ("src/db/updated_draw_weapons.json") as weaponfile:
            all_weapons = json.load(weaponfile)
            for weapon in all_weapons:
                if weapon['rarity'] == "r":
                    self.R_weapons.append(weapon)
                elif weapon['rarity'] == "sr":
                    self.SR_weapons.append(weapon)
                elif weapon['rarity'] == "ssr":
                    self.SSR_weapons.append(weapon)
        return self

    def __pick_unit(self, rarity):
        if rarity == 'r':
            type_of_unit = random.choices(['summon', 'weapon'], [self.R_summons_rate, self.R_weapons_rate], k=1)[0]
            if type_of_unit == 'summon':
                return random.choice(self.R_summons)
            else:
                return random.choice(self.R_weapons)
        elif rarity == 'sr':
            type_of_unit = random.choices(['summon', 'weapon'], [self.SR_summons_rate, self.SR_weapons_rate], k=1)[0]
            if type_of_unit == 'summon':
                return random.choice(self.SR_summons)
            else:
                return random.choice(self.SR_weapons)
        elif rarity == 'ssr':
            type_of_unit = random.choices(['summon', 'weapon'], [self.SSR_summons_rate, self.SSR_weapons_rate], k=1)[0]
            if type_of_unit == 'summon':
                return random.choice(self.SSR_summons)
            else:
                return random.choice(self.SSR_weapons)
    
    def __check_db(self):
        for i in range(10):
            self.__pick_unit('r')
