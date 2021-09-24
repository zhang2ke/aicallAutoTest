import os
from common import utils
from workFlow.botserverApi import BotserverApi
from testCase.testBase import TestBase
import random
import unittest
from workFlow.dbEnvRestore import OpAibot, OpAimatrix

test_data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "testData", "botserverTestData.yaml")
IF_DEBUG = False
DEBUG_MSG = "调试其他用例"


class BotServerTestCase(TestBase):
    """botServer接口用例"""
    botserver_api = None
    op_aibot = None
    op_aimatrix = None
    bot_id, flow_id = None, None

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info("###############开始执行:%s###############" % cls.__doc__)
        super().setUpClass()

        # 获取测试数据
        cls.logger.info("###############测试用例执行前准备")
        cls.logger.info("###############1.获取测试环境和确认测试数据")
        cls.test_data = utils.read_yaml(test_data_file)
        cls.env_info = cls.test_data["env_info"]

        # 创建botserver接口对象
        cls.logger.info("###############2.创建botserver接口对象,初始化")
        cls.botserver_api = BotserverApi(cls.test_data, cls.logger)

        # 创建aibot数据库操作对象
        cls.logger.info("###############3.建立{0}、{1}数据库连接，用于操作数据库".format(cls.env_info["aibot_db_name"], cls.env_info["aicall_db_name"]))
        cls.op_aibot = OpAibot(cls.env_info["db_ip"], cls.env_info["db_port"], cls.env_info["db_user"], cls.env_info["db_pwd"], cls.env_info["aibot_db_name"])
        cls.op_aimatrix = OpAimatrix(cls.env_info["db_ip"], cls.env_info["db_port"], cls.env_info["db_user"], cls.env_info["db_pwd"], cls.env_info["aicall_db_name"])

        # 创建测试数据：机器人和话术流程
        cls.logger.info("###############4.创建测试数据:机器人和话术流程")
        cls.bot_id = cls.botserver_api.create_bot()["data"]["botId"]
        cls.flow_id = cls.botserver_api.create_bot_flow(cls.bot_id)["data"]["flowId"]

        cls.logger.info("###############测试用例执行前准备完成,开始执行测试用例###############\n")

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.botserver_api.http_conn.close_session()
        cls.op_aibot.del_bot(cls.bot_id)
        cls.op_aimatrix.del_speech_engine(cls.bot_id)
        cls.op_aibot.del_flow(cls.flow_id)
        cls.op_aibot.disconnect()
        cls.op_aimatrix.disconnect()
        cls.logger.info("###############%s执行完成###############\n" % cls.__doc__)

    def setUp(self) -> None:
        try:
            self.logger.info("开始执行测试用例##%s##, 该用例对应方法名称:%s" % (self._testMethodDoc, self._testMethodName))
            self.logger.info("首先确认前置条件...")

            # 确认测试数据-机器人id、流程id存在
            bot_data = self.op_aibot.query_bot(self.bot_id)
            if bot_data is None:
                self.skip_msg = "数据库中不存在id为{0}的机器人".format(self.bot_id)
                raise Exception
            flow_data = self.op_aibot.query_flow(self.flow_id)
            if flow_data is None:
                self.skip_msg = "数据库中不存在id为{0}的话术流程".format(self.flow_id)
                raise Exception
            self.logger.info("确认前置条件成功，开始执行用例")
        except Exception as e:
            self.logger.error("确认前置条件发生异常，跳过测试用例##{0}##,异常消息:-{1}".format(self._testMethodDoc, e))
            self.skipTest(self.skip_msg)

    def tearDown(self) -> None:
        self.logger.info("##%s##执行完成\n" % self._testMethodDoc)

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test001_create_bot(self):
        """测试新建机器人"""
        # step: 创建机器人
        self.logger.info("Step1: 新建机器人")
        create_bot_res = self.botserver_api.create_bot()
        bot_id = create_bot_res["data"]["botId"]
        try:
            # Verify: 验证创建机器人是否成功
            self.logger.info("Verify: 验证新建机器人接口是否返回正确响应")
            if create_bot_res["code"] == "921128":
                self.logger.error("模型绑定失败")
            if create_bot_res["code"] == "911119":
                self.logger.error("机器人名称重复")
            self.verify_result(create_bot_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中新增的机器人数据")
            self.op_aibot.del_bot(bot_id)
            self.op_aimatrix.del_speech_engine(bot_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test002_add_flow(self):
        """测试新增话术流程"""
        # step: 对机器人新增流程
        self.logger.info("Step: 对测试数据中机器人{0}新建话术流程".format(self.bot_id))
        add_flow_res = self.botserver_api.create_bot_flow(self.bot_id)
        try:
            # Verify: 验证新增机器人流程是否成功
            self.logger.info("Verify: 验证新建话术流程接口是否返回正确响应")
            self.verify_result(add_flow_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中新建的话术流程数据")
            self.op_aibot.del_flow(add_flow_res["data"]["flowId"])
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test003_remove_flow(self):
        """测试删除机器人流程"""
        # step1: 对机器人新增流程
        self.logger.info("Step1: 对测试数据中机器人{0}新建话术流程".format(self.bot_id))
        add_flow_res = self.botserver_api.create_bot_flow(self.bot_id)
        flow_id = add_flow_res["data"]["flowId"]
        self.logger.info("Step2: 删除话术流程{0}".format(flow_id))
        del_flow_res = self.botserver_api.del_bot_flow(self.bot_id, flow_id)
        try:
            # Verify: 验证新增机器人流程是否成功
            self.logger.info("Verify: 验证删除话术流程接口是否返回正确响应")
            self.verify_result(del_flow_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中新建的话术流程数据")
            self.op_aibot.del_flow(flow_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test004_add_entity(self):
        """测试新增实体"""
        # step: 对机器人创建一个实体
        self.logger.info("Step: 对机器人创建一个实体")
        add_entity_res = self.botserver_api.add_entity(self.bot_id)
        try:
            # Verify: 验证创建实体是否成功
            self.logger.info("Verify: 验证新增实体接口是否返回正确响应")
            self.verify_result(add_entity_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中新建的实体数据")
            self.op_aibot.del_entity(add_entity_res["data"])
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test005_remove_entity(self):
        """测试删除实体"""
        entity_id = None
        try:
            # step: 对机器人创建一个实体
            self.logger.info("Step1: 对机器人创建一个实体")
            add_entity_res = self.botserver_api.add_entity(self.bot_id)
            entity_id = add_entity_res["data"]

            # step2: 对机器人删除实体
            self.logger.info("Step2: 对机器人删除实体")
            del_entity_res = self.botserver_api.del_entity(entity_id)

            # Verify: 验证删除实体是否成功
            self.logger.info("Verify: 验证删除实体接口是否返回正确响应")
            self.verify_result(del_entity_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中新建的实体数据")
            if "entity_id" in locals().keys():
                self.op_aibot.del_entity(entity_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test006_add_intent(self):
        """测试新增意图"""
        entity_id = None
        intent_id = None
        try:
            # step1: 对机器人创建一个实体
            self.logger.info("Step1: 对机器人创建一个实体")
            add_entity_res = self.botserver_api.add_entity(self.bot_id)
            entity_id = add_entity_res["data"]

            # step2: 对机器人创建一个意图
            self.logger.info("Step2: 对机器人创建一个基于实体(实体ID：{0})的意图".format(entity_id))
            add_intent_res = self.botserver_api.add_intent(self.bot_id, entity_id)
            intent_id = add_intent_res["data"]["intentId"]

            # Verify: 验证创建意图是否成功
            self.logger.info("Verify: 验证新增意图接口是否返回正确响应")
            self.verify_result(add_intent_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean1: 清理测试环境数据库中新建的意图数据")
            self.op_aibot.del_intent(intent_id)
            self.logger.info("Clean2: 清理测试环境数据库中新建的实体数据")
            self.op_aibot.del_entity(entity_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test007_remove_intent(self):
        """测试删除意图"""
        entity_id = None
        intent_id = None
        try:
            # step1: 对机器人创建一个实体
            self.logger.info("Step1: 对机器人创建一个实体")
            add_entity_res = self.botserver_api.add_entity(self.bot_id)
            entity_id = add_entity_res["data"]

            # step2: 对机器人创建一个意图
            self.logger.info("Step2: 对机器人创建一个基于实体(实体ID：{0})的意图".format(entity_id))
            add_intent_res = self.botserver_api.add_intent(self.bot_id, entity_id)
            intent_id = add_intent_res["data"]["intentId"]

            # step3: 删除新增的意图
            self.logger.info("Step3: 删除意图(对应ID为{0})".format(intent_id))
            del_intent_res = self.botserver_api.del_intent(intent_id)

            # Verify: 验证创建意图是否成功
            self.logger.info("Verify: 验证新增意图接口是否返回正确响应")
            self.verify_result(del_intent_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean1: 清理测试环境数据库中新建的意图数据")
            self.op_aibot.del_intent(intent_id)
            self.logger.info("Clean2: 清理测试环境数据库中新建的实体数据")
            self.op_aibot.del_entity(entity_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test008_add_tag(self):
        """测试新增轨迹"""
        try:
            # step1: 对机器人新增一个轨迹
            self.logger.info("Step1: 对机器人创建一个轨迹")
            add_tag_res = self.botserver_api.add_tag(self.bot_id)

            # Verify: 验证标签是否创建成功
            self.logger.info("Verify: 验证创建轨迹接口是否返回正确响应")
            self.verify_result(add_tag_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            tag_id = self.op_aibot.query_tag_id(self.bot_id, self.test_data["add_tag"]["tag_name"])
            self.logger.info("Clean: 清理测试环境数据库中新建的轨迹数据")
            self.op_aibot.del_tag(tag_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test009_remove_tag(self):
        """测试删除轨迹"""
        tag_id = None
        try:
            # step1: 对机器人新增一个轨迹
            self.logger.info("Step1: 对机器人创建一个轨迹")
            self.botserver_api.add_tag(self.bot_id)
            tag_id = self.op_aibot.query_tag_id(self.bot_id, self.test_data["add_tag"]["tag_name"])
            if not tag_id:
                self.logger.error("数据库中未查找到bot_id为{0},tag_name为{1}的数据".format(self.bot_id, self.test_data["add_tag"]["tag_name"]))
                raise

            # step2: 删除新建的轨迹
            self.logger.info("Step2: 对机器人删除轨迹")
            del_tag_res = self.botserver_api.del_tag(tag_id)

            # Verify: 验证标签是否创建成功
            self.logger.info("Verify: 验证创建轨迹接口是否返回正确响应")
            self.verify_result(del_tag_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中新建的轨迹数据")
            self.op_aibot.del_tag(tag_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test010_edit_blue_dot(self):
        """测试编辑小蓝点"""
        intent_name = "编辑小蓝点" + str(random.randint(1000, 9999))
        try:
            # step1: 对流程编辑小蓝点后保存
            self.logger.info("Step1: 对流程(flow_id: {0})编辑小蓝点后保存".format(self.flow_id))
            edit_blue_dot_res = self.botserver_api.edit_blue_dot(self.bot_id, self.flow_id, intent_name)

            # Verify: 验证保存小蓝点是否成功
            self.logger.info("Verify: 验证保存小蓝点接口是否返回正确响应")
            self.verify_result(edit_blue_dot_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 清理测试环境数据库中小蓝点数据")
            self.op_aibot.del_blue_dot(self.bot_id, intent_name)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test011_edit_flow_data(self):
        """测试保存话术流程"""
        # intent_id, entity_id = None, None
        try:
            # # step1: 对机器人新增实体
            # self.logger.info("Step1: 对机器人创建一个实体")
            # entity_id = self.botserver_api.add_entity()["data"]
            #
            # # step2: 对机器人新增意图
            # self.logger.info("Step2: 对机器人创建一个完整意图(基于实体包含槽位)")
            # intent_id = self.botserver_api.add_intent(entity_id)["data"]["intentId"]

            # step1: 对流程新增话术并保存
            flow_file = os.path.join('\\'.join(os.path.abspath(__file__).split('\\')[0:-2]), "testData", self.test_data["flow_data"]["file_name"])
            self.logger.info("Step: 对流程保存话术，流程文件路径为:{0}".format(flow_file))
            if not os.path.exists(flow_file):
                self.logger.info("流程数据文件:{0}不存在".format(flow_file))
                raise ("流程数据文件:{0}不存在".format(flow_file))
            edit_flow_res = self.botserver_api.edit_flow_data(self.bot_id, self.flow_id, flow_file)

            # Verify: 验证流程话术是否保存成功
            self.logger.info("Verify: 验证保存话术接口是否返回正确响应")
            self.verify_result(edit_flow_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            # self.logger.info("Clean1: 清理测试环境数据库中新建的意图数据")
            # self.op_aibot.del_intent(intent_id)
            # self.logger.info("Clean2: 清理测试环境数据库中新建的实体数据")
            # self.op_aibot.del_entity(entity_id)
            self.logger.info("Clean3: 从数据库中还原流程数据")
            self.op_aibot.clean_flow_data(self.flow_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test012_bind_engine(self):
        """测试绑定语音引擎"""
        try:
            # step: 对机器人进行绑定语音引擎
            self.logger.info("Step: 对机器人进行绑定语音引擎")
            bind_engine_res = self.botserver_api.rest_api.bind_speech_engine(self.bot_id)

            # Verify: 验证绑定语音引擎是否成功
            self.logger.info("Verify: 验证绑定语音引擎接口是否返回正确响应")
            self.verify_result(bind_engine_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean: 从数据库中还原机器人语音引擎绑定状态")
            self.op_aimatrix.cancel_bind_speech_engine(self.bot_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test013_bot_online(self):
        """测试机器人上线"""
        try:
            # step1: 对流程新增话术并保存
            flow_file = os.path.join('\\'.join(os.path.abspath(__file__).split('\\')[0:-2]), "testData", self.test_data["flow_data"]["file_name"])
            self.logger.info("Step1: 对流程编辑话术，流程文件路径为:{0}".format(flow_file))
            if not os.path.exists(flow_file):
                self.logger.info("流程数据文件:{0}不存在".format(flow_file))
                raise ("流程数据文件:{0}不存在".format(flow_file))
            self.botserver_api.edit_flow_data(self.bot_id, self.flow_id, flow_file)

            bot_status = self.op_aibot.get_bot_status(self.bot_id)
            if bot_status == 1:
                raise Exception("机器人(ID:{0})已经为上线状态，无法进行上线操作".format(self.bot_id))

            # step2: 对机器人进行绑定语音引擎操作
            self.logger.info("Step2: 对机器人进行绑定语音引擎")
            self.botserver_api.rest_api.bind_speech_engine(self.bot_id)

            # step3: 对机器人进行上线操作
            self.logger.info("Step3: 对机器人进行上线操作")
            on_line_res = self.botserver_api.bot_on_line(self.bot_id)

            # Verify: 验证机器人上线是否成功
            self.logger.info("Verify: 验证机器人上线接口是否返回正确响应")
            self.verify_result(on_line_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean1: 从数据库中还原流程数据")
            self.op_aibot.clean_flow_data(self.flow_id)
            self.logger.info("Clean2: 从数据库中还原机器人状态")
            self.op_aibot.bot_off_line(self.bot_id)
            self.logger.info("Clean3: 从数据库中还原机器人语音引擎绑定状态")
            self.op_aimatrix.cancel_bind_speech_engine(self.bot_id)
            self.logger.info("End: 结束测试")

    @unittest.skipIf(IF_DEBUG, reason=DEBUG_MSG)
    def test014_bot_offline(self):
        """测试机器人下线"""
        try:
            # step1: 对流程新增话术并保存
            flow_file = os.path.join('\\'.join(os.path.abspath(__file__).split('\\')[0:-2]), "testData", self.test_data["flow_data"]["file_name"])
            self.logger.info("Step1: 对流程编辑话术，流程文件路径为:{0}".format(flow_file))
            if not os.path.exists(flow_file):
                self.logger.info("流程数据文件:{0}不存在".format(flow_file))
                raise ("流程数据文件:{0}不存在".format(flow_file))
            self.botserver_api.edit_flow_data(self.bot_id, self.flow_id, flow_file)

            # step2: 对机器人进行绑定语音引擎操作
            self.logger.info("Step2: 对机器人进行绑定语音引擎")
            self.botserver_api.rest_api.bind_speech_engine(self.bot_id)

            # step3: 对机器人进行上线操作
            self.logger.info("Step3: 对机器人进行上线操作")
            bot_status = self.op_aibot.get_bot_status(self.bot_id)
            if bot_status == 1:
                raise Exception("机器人(ID:{0})已经为上线状态，无法进行上线操作".format(self.bot_id))
            self.botserver_api.bot_on_line(self.bot_id)

            # step4: 对机器人进行下线操作
            self.logger.info("Step4: 对机器人%s进行下线操作" % self.bot_id)
            bot_status = self.op_aibot.get_bot_status(self.bot_id)
            if bot_status == 0:
                raise Exception("机器人(ID:{0})已经为下线状态，无法进行下线操作".format(self.bot_id))
            off_line_res = self.botserver_api.bot_off_line(self.bot_id)

            # Verify: 验证机器人上线是否成功
            self.logger.info("Verify: 验证机器人下线接口是否返回正确响应")
            self.verify_result(off_line_res, msg="用例:{0}执行失败".format(self._testMethodDoc))
        except Exception as e:
            self.logger.error("测试出现异常,提前终止,异常信息为{0}".format(e))
        finally:
            # 还原测试环境
            self.logger.info("Clean1: 从数据库中还原流程数据")
            self.op_aibot.clean_flow_data(self.flow_id)
            self.logger.info("Clean2: 从数据库中还原机器人状态")
            self.op_aibot.bot_off_line(self.bot_id)
            self.logger.info("Clean3: 从数据库中还原机器人语音引擎绑定状态")
            self.op_aimatrix.cancel_bind_speech_engine(self.bot_id)
            self.logger.info("End: 结束测试")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTest(loader.loadTestsFromTestCase(BotServerTestCase))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
