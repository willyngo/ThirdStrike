class StrikeList:
    def __init__(self):
        self._data = {}

    def __if_exists(self, member_id):
        return str(member_id) in self._data

    def add_strike(self, member_id, reason):
        key = str(member_id)
        if key not in self._data:
            new_strike_list = [reason]
            self._data[key] = new_strike_list
        else:
            self._data[key].append(reason)

    """
    Returns the last strike reason for given member id
    """
    def get_last_strike(self, member_id):
        if self.__if_exists(member_id):
            return self._data[str(member_id)][-1]

    """
    Returns list of all strike reasons for given member id
    """
    def get_all_strikes_for_member(self, member_id):
        if self.__if_exists(member_id):
            return self._data[str(member_id)]

    def remove_last_strike(self, member_id):
        if self.__if_exists(member_id):
            return self._data[str(member_id)].pop(-1)



