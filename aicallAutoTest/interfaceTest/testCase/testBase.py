import unittest
from common.log import Logger


class TestBase(unittest.TestCase):
    # 生成打印日志对象
    logger = Logger().get_logger()

    def verify_result(self, result, msg):
        try:
            if isinstance(result, dict) and ("code" in result or "statusCode" in result) :
                status_code = result["code"] if "code" in result else result["statusCode"]
                if "000000" == status_code :
                    self.logger.info("Result: 验证通过")
                else :
                    self.logger.error("Result: 验证失败,请查看详细的请求及响应信息")
                self.assertTrue("000000" == status_code, msg=msg)
            else :
                self.logger.error("Result: 验证失败,请查看详细的请求及响应信息")
                self.assertTrue(False, msg=msg)
        except Exception as e:
            pass
