import pymongo
import datetime

class mikro_mongo:
    def __init__(self):
        self.myclient = pymongo.MongoClient(
            "mongodb://127.0.0.1:27017/"
        )
        self.mydb = self.myclient["mikro_ops"]
        self.details = self.mydb["details"]
        self.date = datetime.datetime.now()

    def insert_loc(self,location,ipadd,ippub):
        loc = {
            "location": location,
            "ipadd": ipadd,
            "ip_public":ippub,
            "status": 'active',
            "date":self.date,
            }
        self.details.insert_one(loc)

    def select_loc_ip(self, location):
        for dict in self.details.find():
            loc = dict["location"]
            ipadd = dict["ipadd"]
            if loc == location:
                return ipadd

    def select_loc_active(self):
        list=[]
        for dict in self.details.find():
            act = dict["status"]
            loc= dict["location"]
            if act == 'active':
                list.append(loc)
        return list

    def select_loc_deactive(self):
        list=[]
        for dict in self.details.find():
            act = dict["status"]
            loc= dict["location"]
            if act == 'deactive':
                list.append(loc)
        return list

    def deactive_loc(self,loc):
        self.details.update_one({"location": loc}, {"$set": {"status": "deactive"}})

    def active_loc(self,loc):
        self.details.update_one({"location": loc}, {"$set": {"status": "active"}})
