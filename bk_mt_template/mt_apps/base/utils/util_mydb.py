import pymysql


class DbClass():
    def __init__(self, host, port, user, password, db=None, charset="utf8", cursorclass=pymysql.cursors.SSDictCursor):
        self.host = host
        self.user = user
        self.password = password
        self.database = db
        self.port = port
        self.charset = charset
        self.cursorclass = cursorclass
        try:
            self.conn = pymysql.connect(
                host=self.host,
                db=self.database,
                user=self.user,
                passwd=self.password,
                port=self.port,
                charset=self.charset,
                cursorclass=self.cursorclass)
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise e

    def select_db(self, dbname):
        try:
            self.conn.select_db(dbname)
        except Exception as e:
            raise e

    def query_sql(self, sql):
        if self.cursorclass != pymysql.cursors.SSDictCursor:
            raise Exception('DbClass init must be cursorclass = pymysql.cursors.SSDictCursor')
        try:
            self.cursor.execute(sql)
            while True:
                rows = self.cursor.fetchone()
                if rows:
                    yield rows
                else:
                    break
        except Exception as e:
            raise e
        finally:
            self.close_db()

    def query_by_page(self, sql, page_num=1, page_size=10, where_params=None):
        if self.cursorclass != pymysql.cursors.Cursor:
            raise Exception('DbClass init must be cursorclass = pymysql.cursors.Cursor')
        try:
            total = self.cursor.execute(sql, where_params)
            sql = sql + " " + "limit %s, %s"
            offset = (page_num - 1) * page_size
            limit_params = [offset, page_size]
            all_params = []
            if where_params:
                all_params.extend(where_params)
            all_params.extend(limit_params)
            self.cursor.execute(sql, all_params)
            all_res = self.cursor.fetchall()

            data = {
                'result': [dict(zip([temp[0] for temp in self.cursor.description], data)) for data in all_res],
                'count': int(total)
            }
            return data

        except Exception as e:
            raise e
        finally:
            self.close_db()

    def commit(self):
        self.conn.commit()

    def close_db(self):
        self.cursor.close()
        self.conn.close()
