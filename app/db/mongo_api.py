# 导入相应的包
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


def get_now_str():
    dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')


rqk = 'mongodb://admin:cjdg123456@cloud.renqiukai.com:27017/rqk?authSource=admin'
rtw = 'mongodb://admin:cjdg123456@rtw.renqiukai.com:27017/rqk?authSource=admin'


class base:
    db_name = ""
    collection_name = ""
    connection_string = rtw

    def __init__(self):
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def create(self, doc):
        doc["create_time"] = get_now_str()
        doc["update_time"] = get_now_str()
        ret = self.collection.insert_one(doc)
        # print(dir(ret))
        _id = ret.inserted_id
        return self.read(_id)

    def read(self, _id):
        result = self.collection.find_one({"_id": ObjectId(_id)})
        result["_id"] = str(result["_id"])
        return result
        # return self.collection.find_one({"_id": _id})

    def update(self, _id, doc):
        doc["update_time"] = get_now_str()
        ret = self.collection.update_one({"_id": ObjectId(_id)}, {"$set": doc})
        return self.read(_id)

    def delete(self, _id):
        return self.update(_id, dict(delete_flag=1))

    def restore(self, _id):
        return self.update(_id, dict(delete_flag=0))

    def remove(self, _id):
        return self.collection.delete_one({"_id": ObjectId(_id)})

    def list(self, condition=None, fields=None, page_num=1, page_size=10, sort=[("_id", 1)], id_str=False):
        # {$regex:"runoob"}
        data = []
        rows = self.collection.find(
            condition,
            fields
        ).sort(
            sort
        ).limit(
            page_size
        ).skip(
            (page_num-1)*page_size
        )
        for row in rows:
            if id_str:
                row["_id"] = str(row["_id"])
            yield row

    def count(self, filter={}):
        return self.collection.count_documents(filter)


class rqkCollection(base):
    connection_string = rqk
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
    # mid = r.max_tid()
    # rows = r.list(fields=fields, sort=sort)
    # for row in rows:
    #     print(row, mid)
    # print(r.max_tid())
    print(r.count({}))
