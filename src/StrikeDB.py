import json
from discord.ext import commands
from discord import Member

class StrikeDB:
    # def __init__(self, discord_id):
    #     self.strike_count = 0
    #     self.crystal = 0
    #     self.id = discord_id
    #     self.daily = False
    def __init__(self):
        self.__log("Initialize", "Going in")
        self.__getDB()
        self.__log("Initialize", "db has been set up")
    
    '''
    Retrives user in json file from given discord id
    '''
    def getUser(self, author):
        self.__log("getUser", "Going in")
        found = ""
        for user in self.db:
            if user['id'] == author.id:
                found = user
        
        if not found:
            self.__log("getUser", "Could not find user! Will be adding him now.")
            found = self.addUser(author.id, author.name)

        return found
    
    def addUser(self, id, username):
        self.__log("addUser", "Going in")
        user = {
            "id": id,
            "username":username,
            "crystal": 30000,
            "strike_list":[],
            "strikes":0,
            "daily":False
        }
        self.db.append(user)
        self.__updateDB()
        self.__log("addUser", f"Added new user: {username}.")
        return user

    def getDaily(self, author):
        self.__log("getdaily", "Going in")
        user = self.getUser(author)
        
        if not user['daily']:
            user['crystal'] += 3000
            user['daily'] = True
            self.__updateDB()
            return True
        return False
    
    def resetDaily(self):
        self.__log("resetDaily", "Going in")
        for user in self.db:
            user['daily'] = False
        self.__updateDB()



    def addCrystal(self, author, toAdd):
        self.__log("addCrystal", "Going in")
        user = self.getUser(author)

        if user:
            user['crystal'] += int(toAdd)
            self.__log("Addcrystal", f"Added crystal, new total is {user['crystal']}.")
            self.__updateDB()
        else:
            raise commands.UserNotFound(author.name)
    
    def removeCrystal(self, author, toRemove):
        user = self.getUser(author)

        if user:
            user['crystal'] -= int(toRemove)
            self.__log("Addcrystal", f"Removed crystal, new total is {user['crystal']}.")
            self.__updateDB()
        else:
            raise commands.UserNotFound(author.name)
    
    def getCrystal(self, author):
        self.__log("getCrystal", "Going in")
        user = self.getUser(author)

        if user:
            return user['crystal']
    
    def addStrike(self, author, reason):
        self.__log("addStrike", "Going in")
        user = self.getUser(author)

        if user:
            user['strikes'] += 1
            user['strike_list'].append(reason)
            self.__log("addStrike", f"Added strike to {author.name}")
            self.__updateDB()
        else:
            raise commands.UserNotFound(author.name)
    
    def getStrikes(self, author):
        self.__log("getLastStrike", "going in")
        user = self.getUser(author)

        if user:
            return user['strike_list']
        else:
            raise commands.UserNotFound(author.name)

    def removeStrike(self, author):
        self.__log("removeStrike", "Going in")
        user = self.getUser(author)
        if user:
            user['strikes'] -= 1
            self.__log("addStrike", f"removed strike to {author.name}")
            self.__updateDB()
        else:
            raise commands.UserNotFound(author.name)

    
    def __getDB(self):
        with open("src/db/strike_users.json") as userdb:
            self.db = json.load(userdb)

    def __updateDB(self):
        with open("src/db/strike_users.json", "w") as writeJSON:
            json.dump(self.db, writeJSON, indent=2)

    def __log(self, funcname, msg):
        print(f"[StrikeDB | {funcname}]: {msg}")
