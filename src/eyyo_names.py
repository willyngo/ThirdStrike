nas_list = ["nas", "naasir", "nasjuice", "jusab", "naasir jusab"]
shift_list = ["shift", "shifat", "shiftkun"]
ale_list = ["ale", "alessandro", "ciotola", "shadow"]
sam_list = ["sam", "seaim", "seaim khan", "merikato"]
will_list = ["will", "willy", "willyngo", "ngo", "william"]
mt_list = ["mt", "xeiryn"]
kerm_list = ["kermit", "kerm", "tickle"]
kt_list = ["ponkotsu", "kt"]
derek_list = ["derek", "aashiro"]

def get_memberID_from_name(name):
    username = name.lower()
    if username in nas_list:
        return 109824757918134272
    elif username in shift_list:
        return 108991033517289472
    elif username in ale_list:
        return 110556725186170880
    elif username in sam_list:
        return 109825136563081216
    elif username in will_list:
        return 109452980457082880
    elif username in kerm_list:
        return 84127397128962048
    elif username in mt_list:
        return 84126635648880640
    else:
        return None



def get_name_from_memberID(id):
    switcher = {
        109824757918134272: "nas",
        108991033517289472: "shift",
        110556725186170880: "ale",
        109825136563081216: "sam",
        109452980457082880: "will"
    }
    return switcher.get(id, "No such member for given id")
