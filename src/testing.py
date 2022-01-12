import random
import json
import math
from gbf_roll_simulator import gbf_rolls
from StrikeDB import StrikeDB

gacha = gbf_rolls()

draw_weapon = []
all_weapon = []
new_draw_weapon = []
# with open("src/db/premium_draw_weapons.json") as prem_weapon:
#     draw_weapon = json.load(prem_weapon)

with open ("src/db/R_summons_draw.json") as summonfile:
    all_summons = json.load(summonfile)
    for summon in all_summons:
        entry = {}
        entry['type'] = summon[0]
        entry['name'] = summon[2]
        entry['rarity'] = summon[1]
        new_draw_weapon.append(entry)

with open ("src/db/SR_summons_draw.json") as summonfile:
    all_summons = json.load(summonfile)
    for summon in all_summons:
        entry = {}
        entry['type'] = summon[0]
        entry['name'] = summon[2]
        entry['rarity'] = 'sr'
        new_draw_weapon.append(entry)

with open ("src/db/SSR_summons_draw.json") as summonfile:
    all_summons = json.load(summonfile)
    for summon in all_summons:
        entry = {}
        entry['type'] = summon[0]
        entry['name'] = summon[2]
        entry['rarity'] = 'ssr'
        new_draw_weapon.append(entry)

# with open("src/db/all_weapons_.json", encoding="utf8") as all:
#     all_weapon = json.load(all)


# for weapon in draw_weapon:
#     entry={}
#     entry['type'] = weapon[0]
#     entry['rarity'] = weapon[1]
#     entry['name'] = weapon[2]
#     entry['element'] = weapon[4]
#     entry['weapon-type'] = weapon[3]
#     new_draw_weapon.append(entry)
    
# for weap in draw_weapon:
#     entry = {}
#     for weap_to_compare in all_weapon:
#         if weap[2] == weap_to_compare['name']:
#             entry['id'] = weap_to_compare['id']
#             entry['name'] = weap_to_compare['name']
#             entry['rarity'] = weap[1]
#             #entry['type'] = weap[0]
#             new_draw_weapon.append(entry)
#             break
    

with open("src/db/updated_draw_summons.json", "w") as writeJSON:
    json.dump(new_draw_weapon, writeJSON, indent=2)
