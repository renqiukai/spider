from loguru import logger
from .mysql_api import execSql, execSqlmany
from app.db.db_conf import default


class base:
    def __init__(self, db_params=None) -> None:
        logger.debug(db_params)
        if not db_params:
            self.default = default
        else:
            self.default = db_params

    def list(self, fields: list = None, page_num=1, page_size=1000, condition="", order_by={"id": "asc"}):
        # order_by = {fields:desc/asc}
        order_by = ",".join([f"{f} {s}" for f, s in order_by.items()])
        order_by_str = f"order by {order_by}"
        if not fields:
            fields = "*"
        else:
            fields = ",".join(fields)
            
        sql = f"""
        select {fields} from {self.table_name}
        where 1=1
        {condition}
        {order_by_str}
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
        values = ",".join(["%s" for f in data.keys()])
        data = [list(data.values())]
        # logger.debug(data)
        sql = f"""
        insert into {self.table_name}(`{fields}`)
        values({values});
        """
        result = execSqlmany(sql, arg_list=data, db_params=self.default)
        return result

    def batch_create(self, fields: list, data: list):
        values = ",".join(["%s" for f in fields])
        fields = "`,`".join(fields)
        data = [list(d.values()) for d in data]
        # logger.debug(data)

        sql = f"""
        insert into {self.table_name}(`{fields}`)
        values({values});
        """
        result = execSqlmany(sql, arg_list=data, db_params=self.default)
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

    def batch_delete(self, ids: list):
        sql = f"delete from {self.table_name} where id in ({','.join(ids)})"
        result = execSql(sql, self.default, commit=1)
        return result

    def truncate(self):
        sql = f"truncate table {self.table_name};"
        result = execSql(sql, self.default, commit=1)
        return result
