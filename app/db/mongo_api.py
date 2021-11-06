# 导入相应的包
from pymongo import MongoClient
from bson.objectid import ObjectId

rqk = 'mongodb://admin:cjdg123456@cloud.renqiukai.com:27017/rqk?authSource=admin'
rtw = 'mongodb://admin:cjdg123456@rtw.renqiukai.com:27017/rqk?authSource=admin'


class base:
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

    def list(self, condition={}, fields={}, page_num=1, page_size=10, sort=[("_id", 1)]):
        return self.collection.find(
            condition,
            fields
        ).sort(
            sort
        ).limit(
            page_size
        ).skip(
            (page_num-1)*page_size
        )

    def count(self, filter={}):
        return self.collection.count_documents(filter)


class rqkCollection(base):
    connection_string = rtw
    db_name = "rqk"
    collection_name = "images"

    def max_tid(self,):
        fields = {
            "tid": 1,
        }
        sort = [("tid", -1)]
        rows = r.list(fields=fields, sort=sort, page_num=1)
        if rows:
            return rows[0].get("tid")


if __name__ == "__main__":
    r = rqkCollection()
    fields = {
        "_id": 0,
        "title": 1,
        "url": 1,
        "tid": 1,
    }
    sort = [("tid", -1)]
    mid = r.max_tid()
    rows = r.list(fields=fields, sort=sort)
    # for row in rows:
    #     print(row, mid)
    # print(r.max_tid())
    print(r.count({}))
