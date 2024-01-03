import threading
import pymysql
from pymysql.constants import CLIENT


class MySqlDB(object):

    def __init__(self, config, charset='utf8'):
        self.lock = threading.Lock()
        self.config = config
        self.charset = charset

    def __enter__(self):
        self.conn = self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def _connect(self):
        try:
            conn = pymysql.connect(host=self.config[0], port=self.config[4], user=self.config[1],
                                   passwd=self.config[2], db=self.config[3], charset=self.charset,
                                   client_flag=CLIENT.MULTI_STATEMENTS)
            return conn
        except pymysql.Error as e:
            raise Exception(f"Database connection error: {str(e.args[0])} - {str(e.args[1])}")

    def _execute(self, sql, fetch_all=False, is_commit=False, values=None):
        with self.lock:
            try:
                with self.conn.cursor() as cursor:
                    # 判断values是否是列表或元组的列表（用于批量操作）
                    if values is not None:
                        if isinstance(values, list) and all(isinstance(item, (list, tuple)) for item in values):
                            cursor.executemany(sql, values)
                        else:
                            cursor.execute(sql, values)
                    else:
                        cursor.execute(sql)

                    if is_commit:
                        self.conn.commit()
                    elif fetch_all:
                        result = cursor.fetchall()
                        return result
                    else:
                        result = cursor.fetchone()
                        return result
            except pymysql.Error as e:
                if is_commit:
                    self.conn.rollback()
                raise Exception(f"Database execution error: {e.args[0]} - {e.args[1]}")

    def get_one(self, sql, params=None):
        return self._execute(sql, values=params)

    def get_all(self, sql, params=None):
        return self._execute(sql, fetch_all=True, values=params)

    def crud(self, sql, params=None):
        return self._execute(sql, is_commit=True, values=params)

    def exec_many(self, sql, values):
        return self._execute(sql, is_commit=True, values=values)

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    pass

# # 使用示例
# config = ['localhost', 'root', 'password', 'mydatabase']
#
# with MySqlDB(mysql_info) as db:
#     result = db.get_one("SELECT * FROM users WHERE id=1")
#     print(result)
#
#     result = db.get_all("SELECT * FROM users")
#     print(result)
#
#     db.crud("UPDATE users SET name='John' WHERE id=1")
#
#     sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
#     values = [('Michael', 'michael@example.com'), ('Sarah', 'sarah@example.com')]
#     db.exec_many(sql, values)
