import random
import math
from gbf_roll_simulator import gbf_rolls
from StrikeDB import StrikeDB

gacha = gbf_rolls()

pulls = gacha.ten_pull()
for i in pulls:
    print(i)