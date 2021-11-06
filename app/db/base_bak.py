from .mysql_api import execSql
from app.db.db_conf import default


class base:
    def __init__(self) -> None:
        self.default = default

    def list(self, page_num=1, page_size=1000, condition=""):
        sql = f"""
        select * from {self.table_name}
        where 1=1
        {condition}
        limit {(page_num-1)*page_size},{page_size}
        """
        rows = execSql(sql, self.default)
        if rows:
            return rows

    def get(self, id):
        sql = f"""
        select * from {self.table_name}
        where 1=1
        and id={id}
        """
        rows = execSql(sql, self.default)
        if rows:
            return rows[0]

    def create(self, data: dict):
        fields = ",".join(data.keys())
        values = "','".join([str(s) if s else "" for s in data.values()])
        sql = f"""
        insert into {self.table_name}({fields})
        values('{values}');
        """
        result = execSql(sql, self.default, commit=1)
        return result

    def update(self, id, data: dict):
        data = ",".join([f"{k}='{str(v)}'" for k, v in data.items()])
        sql = f"""
        update {self.table_name} set {data} 
        where id={id};
        """
        result = execSql(sql, self.default, commit=1)
        return result

    def delete(self, id, **kwargs):
        sql = f"delete from {self.table_name} where id={id}"
        result = execSql(sql, self.default, commit=1)
        return result
