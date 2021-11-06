from app.db.mongo_api import base, rqk
from datetime import datetime


def get_now_str():
    dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

class SpiderInfo(base):
    connection_string = rqk
    db_name = "spider"
    collection_name = "spider_info"
    example = {
        "_id": "_id",
        "spider_name": "spider_name",
        "params": "max_page=10&min_page=1",
        "create_time": "create_time",
        "update_time": "update_time",
        "delete_flag": 0,
    }

    def list(self, **kwargs):
        condition = kwargs.get("condition", {})
        delete_flag = condition.get("delete_flag", 0)
        condition["delete_flag"] = delete_flag
        return super().list(**kwargs)

    def create(self, data):
        data["create_time"] = get_now_str()
        data["update_time"] = get_now_str()
        data["delete_flag"] = 0
        # params = data.get("params")
            

        return super().create(data)

    def update(self, _id, data):
        # if "create_time" not in data:
        #     data["create_time"] = get_now_str()
        data["update_time"] = get_now_str()
        return super().update(_id, data)

    def max_id(self, _id):
        resp = self.read(_id)
        question_list = resp.get("question_list")
        max_question_id = 0
        for q in question_list:
            question_id = q.get("question_id")
            if question_id > max_question_id:
                max_question_id = question_id
        return max_question_id+1
