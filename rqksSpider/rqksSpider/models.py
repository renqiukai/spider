from .mongo_api_base import rqk, base


class Video(base):
    connection_string = rqk
    db_name = "spider"
    collection_name = "video"
    example = {
        "_id": "",
        "title": "",
        "url": "",
        "video_url": "",
        "tid": "0",
        "video_type": "",
        "create_time": "",
        "update_time": "",
        "delete_flag": 0,
    }

    def max_tid(self,):
        fields = {
            "tid": 1,
        }
        sort = [("tid", -1)]
        rows = self.list(fields=fields, sort=sort, page_num=1)
        if rows:
            return rows[0].get("tid")

    def random(self):
        from random import randint
        condition = {"rate": None}
        m = self.collection.count_documents(condition)
        rows = self.list(condition=condition,
                         page_num=randint(0, m), page_size=1)
        for row in rows:
            return row
