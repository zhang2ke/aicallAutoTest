from common import utils
from workFlow.httpApi import RequestMain
import time


class PdsApi:
    def __init__(self, test_data, logger):
        self.http_conn = RequestMain()
        self.test_data = test_data
        self.logger = logger
        self.service_ip = self.test_data["env_info"]["service_ip"]
        self.service_port = self.test_data["env_info"]["service_port"]
        self.app_id = self.test_data["login_info"]["app_id"]

        self.quest_header = {"Content-Type": "application/json;charset=UTF-8"}

    def create_task(self, bot_id):
        """创建任务"""
        try:
            task_info = self.test_data["create_task"]
            url = utils.get_url(self.service_ip, self.service_port, task_info["url_path"])
            quest_body = {"appid": str(self.app_id), "bot_id": bot_id,
                          "task_id": task_info["task_id"], "task_name": task_info["task_name"], "task_desc": "",
                          "start_date": "{0} 00:00:00".format(time.strftime("%Y-%m-%d", time.localtime())),
                          "end_date": "{0} 23:59:59".format(time.strftime("%Y-%m-%d", time.localtime())),
                          "max_concurrent": task_info["max_concurrent"], "min_concurrent": task_info["min_concurrent"],
                          "isrecord": 1, "num_dir": "/app/nums/{0}".format(self.app_id), "user_id": 1,
                          "call_policy": []}
            self.logger.info("{0}-请求信息如下: \nurl={1}, \nheader={2}, \nbody={3}".format(self.create_task.__doc__, url, self.quest_header, quest_body))
            create_task_res = self.http_conn.request_main(url=url, headers=self.quest_header, json=quest_body)
            if isinstance(create_task_res, str):
                self.logger.info("{0}返回响应：{1}".format(self.create_task.__doc__, create_task_res))
                return create_task_res
            else:
                text_res = self.http_conn.get_res_text(create_task_res)
                self.logger.info("{0}-响应信息：{1}".format(self.create_task.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.create_task.__doc__, e))
            return "Create task exception: {0}".format(e)

    def control_task(self, command, task_id):
        """
        :function:暂停/重启/终止任务
        :command pause: 暂停任务
                 stop: 终止任务
                 resume: 重启任务
        """
        if command != "stop" and command != "pause" and command != "resume":
            self.logger.error("Control task command {0} is not found, please use cmd stop, pause or resume to control task".format(command))
            raise Exception("Control task command {0} is not found".format(command))
        try:
            control_task = self.test_data["control_task"]
            quest_param = "{0}={1}&{2}={3}&{4}={5}".format(control_task["control_par"], command, control_task["app_par"], self.app_id, control_task["task_par"], task_id,)
            url = utils.get_url(self.service_ip, self.service_port, control_task["url_path"] + "?" + quest_param)
            self.logger.info("{0}任务-请求信息: \nurl={1}, \nheader={2}".format(command, url, self.quest_header))
            control_task_res = self.http_conn.request_main(method="get", url=url, headers=self.quest_header)

            if isinstance(control_task_res, str):
                self.logger.info("{0}任务-响应信息：{1}".format(command, control_task_res))
                return control_task_res
            else:
                text_res = self.http_conn.get_res_text(control_task_res)
                self.logger.info("{0}任务-响应信息：{1}".format(command, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} task exception: {1}".format(command, e))
            return "{0} task exception: {1}".format(command, e)

    def pause_task(self, task_id):
        """暂停任务"""
        return self.control_task("pause", task_id)

    def stop_task(self, task_id):
        """停止任务"""
        return self.control_task("stop", task_id)

    def restart_task(self, task_id):
        """重启任务"""
        return self.control_task("resume", task_id)

    def get_task_detail(self, task_id):
        """获取任务详情"""
        try:
            task_detail = self.test_data["task_detail"]
            url = utils.get_url(self.service_ip, self.service_port, task_detail["url_path"]) + "/{0}".format(task_id)
            self.logger.info("{0}-请求信息: \nurl={1}, \nheader={2}".format(self.get_task_detail.__doc__, url, self.quest_header))
            get_task_detail_res = self.http_conn.request_main(method="get", url=url, headers=self.quest_header)

            if isinstance(get_task_detail_res, str):
                self.logger.info("{0}-响应信息：{1}".format(self.get_task_detail.__doc__, get_task_detail_res))
                return get_task_detail_res
            else:
                text_res = self.http_conn.get_res_text(get_task_detail_res)
                self.logger.info("{0}-响应信息：{1}".format(self.get_task_detail.__doc__, text_res))
                return text_res
        except Exception as e:
            # 捕捉异常
            self.logger.error("{0} exception: {1}".format(self.get_task_detail.__doc__, e))
            return "Get task detail exception: {1}"
