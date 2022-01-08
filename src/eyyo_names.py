
mt_list = ["mt", "xeiryn"]
kerm_list = ["kermit", "kerm", "tickle"]
kt_list = ["ponkotsu", "kt"]
derek_list = ["derek", "aashiro"]
my_dict = {
    109824757918134272: ["nas", "naasir", "nasjuice", "jusab", "naasir jusab"],
    108991033517289472: ["shift", "shifat", "shiftkun"],
    110556725186170880: ["ale", "alessandro", "ciotola", "shadow"],
    109825136563081216: ["sam", "seaim", "seaim khan", "merikato", "erraticassassin" "djsam"],
    109452980457082880: ["will", "willy", "willyngo", "ngo", "william"]
}


def get_memberID_from_name(name):
    name_lower = name.lower()
    for memid in my_dict:
        if name_lower in my_dict[memid]:
            return memid


def get_name_from_memberID(memid):
    return my_dict[memid][0]
