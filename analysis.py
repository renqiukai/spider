import json
import os
from loguru import logger


BASE_PATH = os.path.dirname(__file__)
file = os.path.join(
    BASE_PATH,
    "rqksSpider",
    "rqksSpider",
    "bt.json",
)

with open(file, encoding="utf8") as f:
    rows = json.load(f)


for row in rows[:10]:
    print(row.keys())


class cartTask:
    table_name = "t_cart_task"

    def list(self, status=None, page_num=1, page_size=1000):
        condition = ""
        if status or status in [0, 1, 2]:
            condition += f"and status={status}"

        sql = f"""
        select * from {self.table_name}
        where 1=1
        {condition}
        limit {(page_num-1)*page_size},{page_size}
        """
        logger.debug(sql)
        rows = execSql(sql, joeone_db)
        if rows:
            return rows

    def max_id(self):
        sql = f"""
        select * from {self.table_name}
        order by id desc
        limit 1;
        """
        rows = execSql(sql, joeone_db)
        if rows:
            return rows[0].get("id")
        return 3987469

    def create(self, data: dict):
        fields = ",".join(data.keys())
        values = "','".join([str(s) if s else "" for s in data.values()])
        sql = f"""
        insert into {self.table_name}({fields})
        values('{values}');
        """
        logger.debug(sql)
        result = execSql(sql, joeone_db, commit=1)
        return result

    def update(self, id, data: dict):
        data = ",".join([f"{k}='{str(v)}'" for k, v in data.items()])
        sql = f"""
        update {self.table_name} set {data} 
        where id={id};
        """
        logger.debug(sql)
        result = execSql(sql, joeone_db, commit=1)
        return result

    def update_status(self, id, status=1):
        data = dict(
            status=status
        )
        self.update(id, data)
