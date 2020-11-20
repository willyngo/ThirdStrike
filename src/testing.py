import random
from StrikeList import StrikeList
from eyyo_names import get_memberID_from_name
from eyyo_names import get_name_from_memberID

s = StrikeList()
s.add_strike("willy", "bang")
s.add_strike("willy", "bang")
s.add_strike("nas", "erer")
s.add_strike("shift", "demon")
s.add_strike("sam", "cade")
s.add_strike("shift", "demon")
s.add_strike("sam", "cade")
s.add_strike("shift", "demon")
s.add_strike("sam", "cade")

n = [3]

if n:
    print("est")
#
# response = "```\n"
# slist = s.get_all_strikes()
# for memid in slist:
#     print(f"in loop: {memid}")
#     num = len(slist[memid])
#     name = "test"
#     response += f"{name} \t: {num}\n"
#
# response += "```"
#
# print(response)