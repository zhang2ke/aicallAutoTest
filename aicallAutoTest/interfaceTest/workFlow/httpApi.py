import requests
from common import utils


class RequestMain:
    def __init__(self):
        self.session = requests.session()

    def request_main(self, method="post", url=None, params=None, data=None, json=None, headers=None, **kwargs):
        """
        :param method: 请求方式
        :param url: 请求地址
        :param params: 字典或bytes，作为参数增加到url中
        :param data: data类型传参，字典、字节序列或文件对象，作为Request的内容
        :param json: json传参，作为Request的内容
        :param headers: 请求头，字典
        :param kwargs: 若还有其他的参数，使用可变参数字典形式进行传递
        :return: 返回响应
        """
        # 对异常进行捕获
        try:
            """
            封装request请求，将请求方法、请求地址，请求参数、请求头等信息入参。
            """
            res = self.session.request(method, url, params=params, data=data, json=json, headers=headers, **kwargs)

            # 返回响应
            return res
        except Exception as e:
            # 异常返回
            return "Request exception: {0}".format(e)

    @staticmethod
    def get_res_status(response):
        """
        :param response: 响应数据
        :return: 返回响应状态-整数
        """
        try:
            return response.status_code
        except Exception as e:
            # 异常返回
            return "Get response status exception: {0}".format(e)

    @staticmethod
    def get_res_header(response):
        """
        :param response: 响应数据
        :return: 返回响应头-字典数据结构
        """
        try:
            return response.headers
        except Exception as e:
            # 异常返回
            return "Get response header exception: {0}".format(e)

    @staticmethod
    def get_res_text(response):
        """
        :param response: 响应数据
        :return: 返回响应文本-字典数据结构
        """
        try:
            return utils.parse_json(response.text)
        except Exception as e:
            # 异常返回
            return "Get response text exception: {0}".format(e)

    def close_session(self):
        self.session.close()

