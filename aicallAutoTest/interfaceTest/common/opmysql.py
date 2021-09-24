import logging
import pymysql


src_path = "E:/pythtonProject/interfaseTest"


class OpMysql(object):
    def __init__(self, db_host="192.168.179.28", db_port=3306, visit_user="aicall", visit_pwd="Ytxcc123^!", db_name="aimatrix", link_type=1):
        try:
            self.conn = pymysql.connect(host=db_host, user=visit_user, passwd=visit_pwd, db=db_name, port=db_port, charset='utf8')
            if link_type == 0:
                self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            else:
                self.cur = self.conn.cursor()
        except pymysql.Error as e:
            raise Exception("Error: 连接数据库失败 %d: %s" % (e.args[0], e.args[1]))

    def op_sql(self, sql_cmd):
        try:
            self.cur.execute(sql_cmd)
            self.conn.commit()
        except pymysql.Error as e:
            self.conn.rollback()
            raise Exception("Error: 操作数据出错|%s %d: %s" % (sql_cmd, e.args[0], e.args[1]))

    def select_one(self, sql_cmd):
        try:
            row_affect = self.cur.execute(sql_cmd)
            data = self.cur.fetchone() if row_affect > 0 else None
            self.conn.commit()
            return data
        except pymysql.Error as e:
            raise Exception("Error: 查询单条数据出错|%s %d: %s" % (sql_cmd, e.args[0], e.args[1]))

    def select_multil(self, sql_cmd):
        try:
            row_affect = self.cur.execute(sql_cmd)
            data = self.cur.fetchall() if row_affect > 0 else None
            return data
        except pymysql.Error as e:
            raise Exception("Error: 查询多条数据出错|%s %d: %s" % (sql_cmd, e.args[0], e.args[1]))

    def insert_multil(self, sql_cmd, params):
        try:
            results = self.cur.executemany(sql_cmd, params)
            self.conn.commit()
            result = {"code": "0000", "message": "执行批量插入操作成功", "data": int(results)}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {"code": "9999", "message": "执行批量插入操作失败", "data": []}
            print("数据库错误|insert_multil %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=src_path + "/logs/syserror.log",
                                level=logging.DEBUG,
                                format="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s)")
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def close_db_conn(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()


if __name__ == "__main__":
    test = OpMysql()
    result = test.select_one("select * from aicall_task where task_id='16244433063787970524'")
    for re in result:
        print(re)
    test.close_db_conn()
