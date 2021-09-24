from common import utils
from workFlow.httpApi import RequestMain


class RestApi:
    def __init__(self, test_data, logger):
        self.http_conn = RequestMain()
        self.test_data = test_data
        self.logger = logger
        self.service_ip = self.test_data["env_info"]["service_ip"]
        self.service_port = self.test_data["env_info"]["service_port"]

        # 初始化authorization和token
        self.get_auth_token()
        self.quest_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": self.authorization}

    def get_auth_token(self):
        """获取Authentication和sdk-token"""
        self.logger.info("Login web to get Authentication and sdk-token")
        login_res = self.login_web()
        if isinstance(login_res, dict):
            self.authorization = login_res["data"]["token"]
            self.sdk_token = utils.parse_json(login_res["data"]["sdkToken"])["token"]
            self.logger.info("Get Authentication and sdk-token success")
        else:
            self.logger.error("Get Authentication and sdk-token fail")

    def login_web(self):
        """登录web"""
        try:
            login_info = self.test_data["login_info"]
            url = utils.get_url(self.service_ip, self.service_port, login_info["url_path"])
            headers = {"Content-Type": "application/json;charset=UTF-8"}
            quest_body = {"corpId": login_info["corp_id"],
                          "userName": login_info["user_name"],
                          "password": login_info["pwd"]}
            self.logger.info("{0}-请求信息如下: \nurl={1}, \nheader={2}, \nbody={3}".format(self.login_web.__doc__, url, headers, quest_body))
            login_res = self.http_conn.request_main(url=url, headers=headers, json=quest_body)

            if isinstance(login_res, str):
                self.logger.info("{0}返回响应：{1}".format(self.login_web.__doc__, login_res))
                return login_res
            else:
                text_res = self.http_conn.get_res_text(login_res)
                self.logger.info("{0}-响应信息：{1}".format(self.login_web.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("Login exception: {0}".format(e))
            return "Login exception: {0}".format(e)

    def add_custom(self):
        """新增客户资料"""
        try:
            custom_info = self.test_data["add_custom"]
            url = utils.get_url(self.service_ip, self.service_port, custom_info["url_path"])
            quest_body = {"name": custom_info["custom_name"], "sex": custom_info["sex"],
                          "phone": custom_info["phone"], "phoneLocation": "中国,湖北",
                          "email": "", "address": "", "crmGroupList": [],
                          "remark": "", "crmFieldValuesList": []}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.add_custom.__doc__, url, self.quest_header, quest_body))
            add_custom_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(add_custom_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.add_custom.__doc__, add_custom_res))
                return add_custom_res
            else:
                text_res = self.http_conn.get_res_text(add_custom_res)
                self.logger.info("{0}-响应信息：{1}".format(self.add_custom.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.add_custom.__doc__, e))
            return "Add custom exception: {0}".format(e)

    def query_custom(self, phone):
        """通过号码查询客户信息"""
        try:
            url = utils.get_url(self.service_ip, self.service_port, self.test_data["query_custom"]["url_path"])
            quest_body = {"name": "", "phone": phone, "groupId": None,
                          "forTheLastStartTime": "", "forTheLastEndTime": "", "start": 1, "limit": 10}
            self.logger.info("{0}请求信息如下: \nurl={1}, \nheader={2}, \nbody={3}".format(self.query_custom.__doc__, url, self.quest_header, quest_body))
            query_custom_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(query_custom_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.query_custom.__doc__, query_custom_res))
                return query_custom_res
            else:
                text_res = self.http_conn.get_res_text(query_custom_res)
                self.logger.info("{0}-响应信息：{1}".format(self.add_custom.__doc__, text_res))
                return self.http_conn.get_res_text(query_custom_res)
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.query_custom.__doc__, e))
            return "Query custom exception: {0}".format(e)

    def del_custom(self, custom_id):
        """删除客户资料"""
        try:
            url = utils.get_url(self.service_ip, self.service_port, self.test_data["del_custom"]["url_path"])
            quest_body = {"id": custom_id}
            del_custom_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(del_custom_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.del_custom.__doc__, del_custom_res))
                return del_custom_res
            else:
                return self.http_conn.get_res_text(del_custom_res)
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.del_custom.__doc__, e))
            return "Query custom exception: {0}".format(e)

    def bind_speech_engine(self, bot_id):
        """绑定语音引擎"""
        try:
            speech_engine = self.test_data["speech_engine"]
            url = utils.get_url(self.service_ip, self.service_port, speech_engine["url_path"])
            quest_body = {"botId": bot_id, "asrId": speech_engine["asr_id"], "ttsId": speech_engine["tts_id"],
                          "tts": speech_engine["tts"], "speed": speech_engine["speed"],
                          "volume": speech_engine["volume"], "sensitivity": speech_engine["sensitivity"],
                          "tone": str(speech_engine["tone"])}
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}, \nbody={3}".format(self.bind_speech_engine.__doc__, url, self.quest_header, quest_body))
            bind_speech_engine_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)

            if isinstance(bind_speech_engine_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.bind_speech_engine.__doc__, bind_speech_engine_res))
                return bind_speech_engine_res
            else:
                text_res = self.http_conn.get_res_text(bind_speech_engine_res)
                self.logger.info("{0}-响应信息：{1}".format(self.bind_speech_engine.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.bind_speech_engine.__doc__, e))
