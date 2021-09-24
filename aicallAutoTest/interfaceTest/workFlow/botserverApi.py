import os
import random

from requests_toolbelt import MultipartEncoder
from common import utils
from workFlow.httpApi import RequestMain
from workFlow.restApi import RestApi


rest_data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "testData", "restTestData.yaml")


class BotserverApi:
    def __init__(self, test_data, logger):
        """
        test_data: dic
        logger: logger对象
        """
        self.http_conn = RequestMain()
        self.test_data = test_data
        self.logger = logger

        # 获取botserver测试环境信息
        self.test_data = test_data
        self.env_info = self.test_data["env_info"]
        self.service_ip = self.env_info["service_ip"]
        self.service_port = self.env_info["service_port"]
        self.app_id = str(self.env_info["app_id"])

        # 调用restApi中方法初始化authorization和sdk-token
        self.rest_api = RestApi(utils.read_yaml(rest_data_file), self.logger)

        self.authorization, self.sdk_token = self.rest_api.authorization, self.rest_api.sdk_token
        self.quest_header = {"Content-Type": "application/json;charset=UTF-8", "token": self.sdk_token, "appid": self.app_id}

    def create_bot(self):
        """新建机器人"""
        try:
            add_bot = self.test_data["add_bot"]
            url = utils.get_url(self.service_ip, self.service_port, add_bot["url_path"])
            quest_body = {"botName": add_bot["name"]+str(random.randint(1000, 9999)), "botType": str(add_bot["bot_type"]), "bot_icon": add_bot["image"],
                          "nlpEngine": add_bot["nlp"], "tts": str(add_bot["tts"])}
            multipart_encoder = MultipartEncoder(quest_body)
            quest_header = {"token": self.sdk_token, "appid": self.app_id, "Content-Type": multipart_encoder.content_type}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.create_bot.__doc__, url, quest_header, quest_body))

            add_bot_res = self.http_conn.request_main(url=url, headers=quest_header, data=multipart_encoder)

            if isinstance(add_bot_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.create_bot.__doc__, add_bot_res))
                return add_bot_res
            else:
                text_res = self.http_conn.get_res_text(add_bot_res)
                self.logger.info("{0}-响应信息：{1}".format(self.create_bot.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.create_bot.__doc__, e))

    def create_bot_flow(self, bot_id):
        """新建话术流程"""
        try:
            add_flow = self.test_data["add_flow"]
            url = utils.get_url(self.service_ip, self.service_port, add_flow["url_path"])
            quest_body = {"appId": self.app_id, "botId": bot_id, "flowName": add_flow["flow_name"]+str(random.randint(1000, 9999)),
                          "callType": self.test_data["add_bot"]["bot_type"]}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.create_bot_flow.__doc__, url, self.quest_header, quest_body))
            add_flow_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(add_flow_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.create_bot_flow.__doc__, add_flow_res))
                return add_flow_res
            else:
                text_res = self.http_conn.get_res_text(add_flow_res)
                self.logger.info("{0}-响应信息：{1}".format(self.create_bot_flow.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.create_bot_flow.__doc__, e))

    def del_bot_flow(self, bot_id, flow_id):
        """删除话术流程"""
        try:
            del_flow = self.test_data["del_flow"]
            url = utils.get_url(self.service_ip, self.service_port, del_flow["url_path"])
            quest_body = {"botId": bot_id, "flowId": flow_id, "appId": self.app_id}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.del_bot_flow.__doc__, url, self.quest_header, quest_body))
            del_flow_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(del_flow_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.del_bot_flow.__doc__, del_flow_res))
                return del_flow_res
            else:
                text_res = self.http_conn.get_res_text(del_flow_res)
                self.logger.info("{0}-响应信息：{1}".format(self.del_bot_flow.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.del_bot_flow.__doc__, e))

    def add_entity(self, bot_id):
        """新增实体"""
        try:
            add_entity = self.test_data["add_entity"]
            url = utils.get_url(self.service_ip, self.service_port, add_entity["url_path"])
            quest_body = {"botId": bot_id, "appId": self.app_id, "entityName": add_entity["entity_name"],
                          "entityAlias": add_entity["entityAlias"], "entityDesc": "",
                          "entityType": 1, "regxList": [{"regx": add_entity["regxList"]}]}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.add_entity.__doc__, url, self.quest_header, quest_body))
            add_entity_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(add_entity_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.add_entity.__doc__, add_entity_res))
                return add_entity_res
            else:
                text_res = self.http_conn.get_res_text(add_entity_res)
                self.logger.info("{0}-响应信息：{1}".format(self.add_entity.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.add_entity.__doc__, e))

    def del_entity(self, entity_id):
        """删除实体"""
        try:
            del_entity = self.test_data["del_entity"]
            url = utils.get_url(self.service_ip, self.service_port, del_entity["url_path"])
            quest_body = {"id": entity_id, "appId": self.app_id}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.del_entity.__doc__, url, self.quest_header, quest_body))
            del_entity_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(del_entity_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.del_entity.__doc__, del_entity_res))
                return del_entity_res
            else:
                text_res = self.http_conn.get_res_text(del_entity_res)
                self.logger.info("{0}-响应信息：{1}".format(self.del_entity.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.del_entity.__doc__, e))

    def add_intent(self, bot_id, entity_id):
        """新增意图"""
        try:
            add_intent = self.test_data["add_intent"]
            url = utils.get_url(self.service_ip, self.service_port, add_intent["url_path"])
            quest_body = {"appId": self.app_id,
                          "botId": bot_id,
                          "intention": add_intent["intent_name"],
                          "similarList": [{"similar": add_intent["similar1"]},
                                          {"similar": add_intent["similar2"]}],
                          "ruleList": [{"regx": add_intent["regxList"], "status": 0}],
                          "slotList": [{"slotName": add_intent["sot_name1"],
                                        "slotAlias": add_intent["slotAlias1"],
                                        "entityId": entity_id,
                                        "entityName": self.test_data["add_entity"]["entity_name"],
                                        "entityAlias": self.test_data["add_entity"]["entityAlias"]},
                                       {"slotName": add_intent["sot_name2"],
                                        "slotAlias": add_intent["slotAlias2"],
                                        "entityId": entity_id,
                                        "entityName": self.test_data["add_entity"]["entity_name"],
                                        "entityAlias": self.test_data["add_entity"]["entityAlias"]}]
                          }
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.add_intent.__doc__, url, self.quest_header, quest_body))
            add_intent_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(add_intent_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.add_intent.__doc__, add_intent_res))
                return add_intent_res
            else:
                text_res = self.http_conn.get_res_text(add_intent_res)
                self.logger.info("{0}-响应信息：{1}".format(self.add_intent.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.add_intent.__doc__, e))

    def del_intent(self, intent_id):
        """删除意图"""
        try:
            del_intent = self.test_data["del_intent"]
            url = utils.get_url(self.service_ip, self.service_port, del_intent["url_path"])
            quest_body = {"id": intent_id, "appId": self.app_id}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.del_intent.__doc__, url, self.quest_header, quest_body))
            add_intent_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(add_intent_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.del_intent.__doc__, add_intent_res))
                return add_intent_res
            else:
                text_res = self.http_conn.get_res_text(add_intent_res)
                self.logger.info("{0}-响应信息：{1}".format(self.del_intent.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.del_intent.__doc__, e))

    def add_tag(self, bot_id):
        """增加轨迹"""
        try:
            add_tag = self.test_data["add_tag"]
            url = utils.get_url(self.service_ip, self.service_port, add_tag["url_path"])
            quest_body = {"appId": self.app_id, "botId": bot_id, "tagName": add_tag["tag_name"], "pid": -1}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.add_tag.__doc__, url, self.quest_header, quest_body))
            add_tag_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(add_tag_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.add_tag.__doc__, add_tag_res))
                return add_tag_res
            else:
                text_res = self.http_conn.get_res_text(add_tag_res)
                self.logger.info("{0}-响应信息：{1}".format(self.add_tag.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.add_tag.__doc__, e))

    def del_tag(self, tag_id):
        """删除轨迹"""
        try:
            del_tag = self.test_data["del_tag"]
            url = utils.get_url(self.service_ip, self.service_port, del_tag["url_path"])
            quest_body = {"id": tag_id, "appId": self.app_id}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.del_tag.__doc__, url, self.quest_header, quest_body))
            del_tag_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(del_tag_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.del_tag.__doc__, del_tag_res))
                return del_tag_res
            else:
                text_res = self.http_conn.get_res_text(del_tag_res)
                self.logger.info("{0}-响应信息：{1}".format(self.del_tag.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.del_tag.__doc__, e))

    def edit_blue_dot(self, bot_id, flow_id, blue_intent):
        """编辑小蓝点"""
        try:
            edit_blue_dot = self.test_data["blue_dot"]
            url = utils.get_url(self.service_ip, self.service_port, edit_blue_dot["url_path"])
            quest_body = {"botId": bot_id, "flowId": flow_id, "nodeKey": 0,
                          "botName": self.test_data["bot_info"]["bot_name"], "isFirst": 1,
                          "intentList": [[{"intentName": blue_intent, "intentType": 0}]], "appId": self.app_id}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.edit_blue_dot.__doc__, url, self.quest_header, quest_body))
            edit_blue_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(edit_blue_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.edit_blue_dot.__doc__, edit_blue_res))
                return edit_blue_res
            else:
                text_res = self.http_conn.get_res_text(edit_blue_res)
                self.logger.info("{0}-响应信息：{1}".format(self.edit_blue_dot.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.edit_blue_dot.__doc__, e))

    def edit_flow_data(self, bot_id, flow_id, flow_data_file):
        """编辑话术流程"""
        try:
            save_flow = self.test_data["flow_data"]
            url = utils.get_url(self.service_ip, self.service_port, save_flow["url_path"])
            with open(flow_data_file) as f:
                flow_src_data = f.read().strip("/n")
                f.close()
            quest_body = {"flowId": flow_id, "botId": bot_id, "flowSrcDataCompress": flow_src_data, "flowType": 1, "appId": self.app_id}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.edit_flow_data.__doc__, url, self.quest_header, quest_body))
            save_flow_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(save_flow_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.edit_flow_data.__doc__, save_flow_res))
                return save_flow_res
            else:
                text_res = self.http_conn.get_res_text(save_flow_res)
                self.logger.info("{0}-响应信息：{1}".format(self.edit_flow_data.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.edit_flow_data.__doc__, e))

    def bot_on_line(self, bot_id):
        """机器人上线"""
        try:
            url = utils.get_url(self.service_ip, self.service_port, self.test_data["bot_on_line"]["url_path"])
            quest_body = {"botId": bot_id}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.bot_on_line.__doc__, url, self.quest_header, quest_body))
            on_line_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(on_line_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.bot_on_line.__doc__, on_line_res))
                return on_line_res
            else:
                text_res = self.http_conn.get_res_text(on_line_res)
                self.logger.info("{0}-响应信息：{1}".format(self.bot_on_line.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.bot_on_line.__doc__, e))

    def bot_off_line(self, bot_id):
        """机器人下线"""
        try:
            url = utils.get_url(self.service_ip, self.service_port, self.test_data["bot_off_line"]["url_path"])
            quest_body = {"botId": bot_id}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.bot_off_line.__doc__, url, self.quest_header, quest_body))
            off_line_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(off_line_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.bot_off_line.__doc__, off_line_res))
                return off_line_res
            else:
                text_res = self.http_conn.get_res_text(off_line_res)
                self.logger.info("{0}-响应信息：{1}".format(self.bot_off_line.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.bot_off_line.__doc__, e))
