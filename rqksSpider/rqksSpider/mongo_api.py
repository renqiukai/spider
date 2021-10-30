# 导入相应的包
from pymongo import MongoClient
from bson.objectid import ObjectId

rqk = 'mongodb://admin:123456@cloud.renqiukai.com:27017/rqk?authSource=admin'
rtw = 'mongodb://admin:cjdg123456@rtw.renqiukai.com:27017/rqk?authSource=admin'


class collection:
    db_name = ""
    collection_name = ""
    connection_string = ""

    def __init__(self):
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def create(self, doc):
        ret = self.collection.insert_one(doc)
        # print(dir(ret))
        return ret.inserted_id

    def read(self, _id):
        return self.collection.find_one({"_id": ObjectId(_id)})

    def update(self, _id, doc):
        ret = self.collection.update_one({"_id": ObjectId(_id)}, {"$set": doc})
        return ret.raw_result

    def delete(self, _id):
        return self.update(_id, delete_flag="1")

    def remove(self, _id):
        return self.collection.delete_one({"_id": ObjectId(_id)})

    def list(self, condition={}, fields={}, page_num=1, page_size=10):
        return self.collection.find(condition, fields).limit(page_size).skip((page_num-1)*page_size)


class rqkCollection(collection):
    connection_string = rtw
    db_name = "rqk"
    collection_name = "temp"


if __name__ == "__main__":
    r = rqkCollection()
    for row in r.list(fields={"a":1,"_id":0}):
        print(row)
