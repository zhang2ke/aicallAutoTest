# 该部分未调试完成，暂不可使用
import logging
import redis

src_path = "E:/pythtonProject/interfaseTest"


class OpRedis(object):
    def __init__(self, redis_host="192.168.180.129", redis_port=6379, redis_pwd="ytx666yun", db_no=0):
        try:
            self.redis_cli = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_pwd, db=db_no, decode_responses=True)
        except redis.exceptions.ConnectionError as e:
            raise Exception("Error: 连接redis失败 %d: %s" % (e.args[0], e.args[1]))

    def get(self, key):
        return self.redis_cli.get(key)

    def smembers(self, key):
        return self.redis_cli.smembers(key)

    def delete(self, key):
        return self.redis_cli.delete(key)

    def close_conn(self):
        try:
            self.redis_cli.close()
        except Exception as e:
            raise Exception("Error: 关闭redis失败 %d: %s" % (e.args[0], e.args[1]))


if __name__ == "__main__":
    redis_cli = OpRedis()
    # result = redis_cli.get("aicall002|16273747136549298884")
    # result2 = redis_cli.delete("aicall002|1627374713654929888")
    result3 = redis_cli.smembers("aicall003|90001")

    # print(result)
    # print(result2)
    print(result3)
    redis_cli.close_conn()

