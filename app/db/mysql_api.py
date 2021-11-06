'''
@author: renqiukai
@Date: 2020-06-17 01:22:21
@Description: mysql connection function
@LastEditTime: 2020-06-17 01:32:36
'''
import pymysql
from app.core.logging import logger
from app.db.db_conf import default


def execSql(sql, db_params=default, commit=0, cursor_type="dict"):
    # db_params为参数集合,默认值是cjdg_readonly.
    db = pymysql.connect(**db_params)  # 连接数据库
    if cursor_type == "dict":
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)  # 创建游标。
    else:
        cursor = db.cursor()  # 创建游标。
    logger.debug(sql)
    result = cursor.execute(sql)
    if commit == 1:
        try:
            db.commit()
            return result
        except:
            db.rollback()
            logger.debug("执行错误回滚。")
    else:
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result


def execSqlmany(sql, arg_list, db_params=default, commit=1):
    # db_params为参数集合,默认值是cjdg_readonly.
    db = pymysql.connect(**db_params)  # 连接数据库
    cursor = db.cursor()  # 创建游标。
    logger.debug(sql)
    result = cursor.executemany(sql, arg_list)
    if commit == 1:
        db.commit()
    cursor.close()
    db.close()
    return result


def execSql_pandas(sql, db_params):
    import pandas as pd
    db = pymysql.connect(**db_params)  # 连接数据库
    df = pd.read_sql(sql, con=db)
    result = df
    db.close()
    return result


class etl:
    '''
    1000条一页。
    定义来源的sql。
    定义目的的sql。
    '''
    page_size = 1000

    def __init__(self, page_size=1000):
        self.page_size = page_size

    def read(self, sql, db_params):
        count_sql = f'''
        select count(1) from ({sql}) t;
        '''
        count = execSql(count_sql, db_params, cursor_type="list")[0][0]
        logger.debug(f"count is {count}")
        for page in range(int(count/self.page_size)+1):
            start = page * self.page_size
            set_sql = (f'{sql} limit {start},{self.page_size};')
            logger.debug(set_sql)
            result = execSql(set_sql, db_params, cursor_type="list")
            # logger.debug(result)
            yield result

    def tableInput(self, sql, db_params):
        '''
        表输入方法
        '''
        result = []
        for r in self.read(sql, db_params):
            result += [a for a in r]
        logger.debug("sys_user表数据获取成功。")
        return result

    def tableOutput(self):
        '''
        表输出方法
        '''

    def write(self, sql, arg_list, db_params):
        count = len(arg_list)
        for page in range(int(count/self.page_size)+1):
            start = page * self.page_size
            data = arg_list[start:self.page_size]
            execSqlmany(sql, data, db_params)
            logger.debug("写入成功。")
