import os
from workFlow.restApi import RestApi
from workFlow.dbEnvRestore import OpAimatrix
from common import utils
from testCase.testBase import TestBase
import unittest

test_data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "testData", "restTestData.yaml")
IF_DEBUG = False  # debug 开关
DEBUG_MSG = "调试其他用例"


class RestTestCase(TestBase):
    """rest接口用例"""
    rest_api, op_aimatrix = None, None

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info("###############开始执行测试类:{0}###############".format(cls.__doc__))

        # 获取测试数据
        cls.logger.info("###############测试用例执行前准备")
        cls.logger.info("###############1.获取测试环境和测试数据")
        cls.test_data = utils.read_yaml(test_data_file)
        cls.env_info = cls.test_data["env_info"]

        # rest服务信息
        cls.service_ip = cls.test_data["env_info"]["service_ip"]
        cls.service_post = cls.env_info["service_port"]

        # 创建rest接口和botserver接口对象
        cls.logger.info("###############2.创建rest接口操作对象，用于调用rest接口")
        cls.rest_api = RestApi(cls.test_data, cls.logger)

        # 创建aimatrix数据库操作实例
        cls.logger.info("###############3.建立{0}数据库连接，用于恢复数据库环境".format(cls.env_info["db_name"]))
        cls.op_aimatrix = OpAimatrix(cls.env_info["db_ip"], cls.env_info["db_port"], cls.env_info["db_user"], cls.env_info["db_pwd"], cls.env_info["db_name"])

        cls.logger.info("###############测试用例执行前准备完成,开始执行测试用例###############\n")

    @classmethod
    def tearDownClass(cls):
        cls.rest_api.http_conn.close_session()
        cls.op_aimatrix.disconnect()
        cls.logger.info("###############测试类:{0}执行完成###############\n".format(cls.__doc__))

    def setUp(self) -> None:
        self.logger.info("开始执行测试用例:{0}, 该用例对应方法名称:{1}".format(self._testMethodDoc, self._testMethodName))

    def tearDown(self) -> None:
        self.logger.info("测试用例:{0}执行完成\n".format(self._testMethodDoc))

    @unittest.skipIf(condition=IF_DEBUG, reason=DEBUG_MSG)
    def test001_login_web(self):
        """测试登录web"""
        # step: 登录web
        self.logger.info("Step: 使用测试数据中用户信息登录web")
        login_res = self.rest_api.login_web()

        # verify: 验证登录web是否成功
        self.logger.info("Verify: 验证登录web是否成功")
        self.verify_result(login_res, msg="用例:{0}执行失败".format(self._testMethodDoc))

    @unittest.skipIf(condition=IF_DEBUG, reason=DEBUG_MSG)
    def test002_add_custom(self):
        """测试新建客户资料"""
        try:
            # step: 新建客户资料
            self.logger.info("Step: 新建客户")
            add_custom_res = self.rest_api.add_custom()

            # Verify: 验证新建客户资料是否成功
            self.logger.info("Verify: 验证新建客户资料是否返回正确响应")
            self.verify_result(add_custom_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中客户数据")
            self.op_aimatrix.del_custom(self.test_data["add_custom"]["phone"])
            self.logger.info("End: 结束测试")

    @unittest.skipIf(condition=IF_DEBUG, reason=DEBUG_MSG)
    def test003_query_custom(self):
        """测试查询客户资料"""
        try:
            # step1: 新建客户资料
            self.logger.info("Step1: 新建客户")
            self.rest_api.add_custom()

            # step2: 通过号码查询客户信息
            self.logger.info("Step2: 通过号码-{0}查询客户".format(self.test_data["add_custom"]["phone"]))
            query_custom_res = self.rest_api.query_custom(self.test_data["add_custom"]["phone"])

            # Verify: 验证新建客户资料是否成功
            self.logger.info("Verify: 验证查询客户资料是否返回正确响应")
            self.verify_result(query_custom_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中客户数据")
            self.op_aimatrix.del_custom(self.test_data["add_custom"]["phone"])
            self.logger.info("End: 结束测试")

    @unittest.skipIf(condition=IF_DEBUG, reason=DEBUG_MSG)
    def test004_delete_custom(self):
        """测试删除客户资料"""
        try:
            # step1: 新建客户资料
            self.logger.info("Step1: 新建客户")
            self.rest_api.add_custom()

            # step2: 通过号码查询客户信息
            self.logger.info("Step2: 通过号码-{0}查询客户信息,获取客户ID".format(self.test_data["add_custom"]["phone"]))
            custom_id = self.rest_api.query_custom(self.test_data["add_custom"]["phone"])["data"]["resultList"][0]["id"]

            # step3: 通过号码查询客户信息
            self.logger.info("Step3: 删除客户，客户ID为{0}".format(custom_id))
            delete_custom_res = self.rest_api.del_custom(custom_id)

            # Verify: 验证新建客户资料是否成功
            self.logger.info("Verify: 验证删除客户资料是否返回正确响应")
            self.verify_result(delete_custom_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中客户数据")
            self.op_aimatrix.del_custom(self.test_data["add_custom"]["phone"])
            self.logger.info("End: 结束测试")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(RestTestCase))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
