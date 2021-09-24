import os
from workFlow.pdsApi import PdsApi
from workFlow.botserverApi import BotserverApi
from workFlow.dbEnvRestore import OpAimatrix, OpAibot
from common import utils
from testCase.testBase import TestBase
import time

import unittest

test_data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "testData", "pdsTestData.yaml")
botserver_test_data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "testData", "botserverTestData.yaml")
IF_DEBUG = False  # debug 开关
DEBUG_MSG = "调试其他用例"


class PdsTestCase(TestBase):
    """pds接口用例"""
    pds_api, botserver_api = None, None
    op_aimatrix, op_aibot = None, None
    bot_id, flow_id = None, None

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info("###############开始执行测试类:{0}###############".format(cls.__doc__))

        # 获取测试数据
        cls.logger.info("###############测试用例执行前准备")
        cls.logger.info("###############1.获取测试环境和测试数据")
        cls.test_data = utils.read_yaml(test_data_file)
        cls.botserver_test_data = utils.read_yaml(botserver_test_data_file)
        cls.env_info = cls.test_data["env_info"]

        # 创建接口调用对象
        cls.logger.info("###############2.创建pds接口操作对象，用于调用pds接口")
        cls.pds_api = PdsApi(cls.test_data, cls.logger)
        cls.botserver_api = BotserverApi(cls.botserver_test_data, cls.logger)

        # 创建aimatrix数据库操作实例
        cls.logger.info("###############3.建立{0}和{1}数据库连接，用于恢复数据库环境".format(cls.env_info["aibot_db_name"], cls.env_info["aicall_db_name"]))
        cls.op_aibot = OpAibot(cls.env_info["db_ip"], cls.env_info["db_port"], cls.env_info["db_user"], cls.env_info["db_pwd"], cls.env_info["aibot_db_name"])
        cls.op_aimatrix = OpAimatrix(cls.env_info["db_ip"], cls.env_info["db_port"], cls.env_info["db_user"], cls.env_info["db_pwd"], cls.env_info["aicall_db_name"])

        # 创建测试数据：机器人和话术流程
        cls.logger.info("###############4.创建测试数据:机器人、话术流程、编辑流程、绑定语音引擎、上线机器人")
        cls.bot_id = cls.botserver_api.create_bot()["data"]["botId"]
        cls.flow_id = cls.botserver_api.create_bot_flow(cls.bot_id)["data"]["flowId"]
        flow_file = os.path.join('\\'.join(os.path.abspath(__file__).split('\\')[0:-2]), "testData", cls.botserver_test_data["flow_data"]["file_name"])
        cls.botserver_api.edit_flow_data(cls.bot_id, cls.flow_id, flow_file)
        cls.botserver_api.rest_api.bind_speech_engine(cls.bot_id)
        cls.botserver_api.bot_on_line(cls.bot_id)
        cls.logger.info("###############测试用例执行前准备完成,开始执行测试用例###############\n")

    @classmethod
    def tearDownClass(cls):
        cls.pds_api.http_conn.close_session()
        cls.botserver_api.http_conn.close_session()
        cls.op_aibot.del_bot(cls.bot_id)
        cls.op_aimatrix.del_speech_engine(cls.bot_id)
        cls.op_aibot.del_flow(cls.flow_id)
        cls.op_aimatrix.disconnect()
        cls.logger.info("###############测试类:{0}执行完成###############\n".format(cls.__doc__))

    def setUp(self) -> None:
        self.logger.info("开始执行测试用例:{0}, 该用例对应方法名称:{1}".format(self._testMethodDoc, self._testMethodName))

    def tearDown(self) -> None:
        self.logger.info("测试用例:{0}执行完成\n".format(self._testMethodDoc))

    @unittest.skipIf(condition=IF_DEBUG, reason=DEBUG_MSG)
    def test001_create_task(self):
        """测试创建任务"""
        task_id = None
        try:
            # Step1: 创建任务
            self.logger.info("Step: 使用测试数据中信息创建任务")
            create_task_res = self.pds_api.create_task(self.bot_id)
            task_id = self.test_data["create_task"]["task_id"]
            self.wait_task_status_change(task_id, 1)

            # Verify1: 验证创建任务是否成功
            self.logger.info("Verify: 验证创建任务是否返回正确响应")
            self.verify_result(create_task_res, msg="用例:{0}执行失败".format(self._testMethodDoc))

            self.logger.info("调用终止任务接口还原测试环境")
            self.pds_api.stop_task(task_id)
            self.wait_task_status_change(task_id, 3)
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中客户数据")
            self.op_aimatrix.del_task(task_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(condition=IF_DEBUG, reason=DEBUG_MSG)
    def test002_get_task_detail(self):
        """测试获取任务详情"""
        task_id = None
        try:
            # Step1: 创建任务
            self.logger.info("Step1: 使用测试数据中信息创建任务")
            self.pds_api.create_task(self.bot_id)
            task_id = self.test_data["create_task"]["task_id"]
            self.wait_task_status_change(task_id, 1)

            # Step2: 获取任务详情
            self.logger.info("Step2: 获取上一步创建任务的详细信息")
            get_task_res = self.pds_api.get_task_detail(task_id)

            # Verify2: 验证获取任务详情是否成功
            self.logger.info("Verify2: 验证获取任务详情是否返回正确响应")
            self.verify_result(get_task_res, msg="用例:{0}执行失败".format(self._testMethodDoc))

            self.logger.info("调用终止任务接口还原测试环境")
            self.pds_api.stop_task(task_id)
            self.wait_task_status_change(task_id, 3)
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中客户数据")
            self.op_aimatrix.del_task(task_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(condition=IF_DEBUG, reason=DEBUG_MSG)
    def test003_stop_task(self):
        """测试终止任务"""
        task_id = None
        try:
            # step1: 创建任务
            self.logger.info("Step1: 使用测试数据中信息创建任务")
            self.pds_api.create_task(self.bot_id)
            task_id = self.test_data["create_task"]["task_id"]
            self.wait_task_status_change(task_id, 1)

            # step2: 暂停任务
            self.logger.info("Step2: 终止任务")
            stop_task_res = self.pds_api.stop_task(task_id)
            self.wait_task_status_change(task_id, 3)

            # Verify: 验证终止任务是否成功
            self.logger.info("Verify: 验证终止任务是否成功")
            self.verify_result(stop_task_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中客户数据")
            self.op_aimatrix.del_task(task_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(condition=IF_DEBUG, reason=DEBUG_MSG)
    def test004_pause_resume_task(self):
        """测试暂停/重启任务"""
        task_id = None
        try:
            # step1: 创建任务
            self.logger.info("Step1: 使用测试数据中信息创建任务")
            self.pds_api.create_task(self.bot_id)
            task_id = self.test_data["create_task"]["task_id"]
            self.wait_task_status_change(task_id, 1)

            # step2: 暂停任务
            self.logger.info("Step3: 暂停任务")
            pause_task_res = self.pds_api.pause_task(task_id)
            self.wait_task_status_change(task_id, 5)

            # Verify1: 验证暂停任务是否成功
            self.logger.info("Verify1: 验证暂停任务是否返回正确响应")
            self.verify_result(pause_task_res, msg="用例:{0}执行失败".format(self._testMethodDoc))

            # step3: 重启任务
            self.logger.info("Step4: 重启任务")
            restart_task_res = self.pds_api.restart_task(task_id)
            self.wait_task_status_change(task_id, 1)

            # Verify2: 验证暂停任务是否成功
            self.logger.info("Verify2: 验证重启任务是否成功")
            self.verify_result(restart_task_res, msg="用例:{0}执行失败".format(self._testMethodDoc))

            self.logger.info("调用终止任务接口还原测试环境")
            self.pds_api.stop_task(task_id)
            self.wait_task_status_change(task_id, 3)
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中客户数据")
            self.op_aimatrix.del_task(task_id)
            self.logger.info("End: 结束测试")

    def wait_task_status_change(self, task_id, status):
        """
        等待任务状态发生变化，最长等待1分钟
        task_id: 待查询任务ID
        status： 1-执行中, 2-已完成, 3-已停止, 5-已暂停
        """
        if status != 1 and status != 3 and status != 5:
            self.logger.error("Task status flag {0} is not found, please use 1-执行中, 3-已停止 or 5-已暂停 to wait")
            raise Exception("Task status flag {0} is not found")
        for i in range(60):
            task_status = self.op_aimatrix.query_task_status(task_id)
            if task_status == status:
                return True
            if i >= 59:
                return False
            time.sleep(1)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTest(loader.loadTestsFromTestCase(PdsTestCase))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
