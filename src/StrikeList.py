class StrikeList:
    def __init__(self):
        self._data = {
            109824757918134272: [],
            108991033517289472: [],
            110556725186170880: [],
            109825136563081216: [],
            109452980457082880: []
        }

    def __if_exists(self, member_id):
        return member_id in self._data

    def add_strike(self, member_id, reason):
        if member_id not in self._data:
            new_strike_list = [reason]
            self._data[member_id] = new_strike_list
        else:
            self._data[member_id].append(reason)

    """
    Returns the last strike reason for given member id
    """
    def get_last_strike(self, member_id):
        if self.__if_exists(member_id):
            return self._data[member_id][-1]

    """
    Returns list of all strike reasons for given member id
    """
    def get_all_strikes_for_member(self, member_id):
        if self.__if_exists(member_id):
            return self._data[member_id]

    def remove_last_strike(self, member_id):
        if self.__if_exists(member_id):
            return self._data[member_id].pop(-1)

    def get_all_strikes(self):
        return self._data
