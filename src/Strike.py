class Strike:
    def __init__(self, member_name, reason="None given"):
        self.member_name = member_name
        self.reason = reason

    def set_reason(self, reason):
        self.reason = reason

    def get_reason(self):
        return self.reason

    def set_member(self, name):
        self.member_name = name

    def get_member(self):
        return self.member_name
