import os
from TestRunner import HTMLTestRunner
import unittest
from common.sendEmail import SendEmail
import importlib
import time
from common.log import Logger
from common.textTestReport import TextReport

current_dir = os.path.dirname(__file__)
Report_Bak_Count = 5
Log_Bak_Count = 5
Report_Name = "Aicall_test_report"


class AllTest:
    def __init__(self):
        self.test_result_dir = os.path.join(current_dir, "result")
        self.test_file = os.path.join(current_dir, "testFile.txt")
        self.test_case_Dir = os.path.join(current_dir, "testCase")
        self.test_suite = unittest.TestSuite()
        self.log_dir = os.path.join(current_dir, "log").replace("\\", "/")
        self.logger = Logger().get_logger()

        self.get_case_list()
        self.get_test_suite()
        self.run_test()
        self.clear_history_log()
        self.clear_history_report()
        self.send_report()

    def get_case_list(self):
        """从测试用例文件testFileList.txt中添加到caselist"""
        self.test_fileName_list = []
        fb = open(self.test_file)
        for line in fb.readlines():
            if line.strip("/n") != '' and not line.startswith("#"):
                self.test_fileName_list.append(line.strip("\n"))
        fb.close()

    def get_test_suite(self):
        """装载测试用例集suit列表"""
        suite_module = []
        for case_file_name in self.test_fileName_list:
            test_module = importlib.import_module("testCase.%s" % case_file_name)
            discover = unittest.TestLoader().loadTestsFromModule(test_module, pattern="test*")
            suite_module.append(discover)
        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    self.test_suite.addTest(test_name)
        else:
            self.logger.info('测试集模块为空')
            return None

    def generate_report_name(self):
        """通过时间戳拼接生成测试报告名称"""
        report_name = "{0}_{1}.html".format(Report_Name, time.strftime("%Y%m%d%H%M%S", time.localtime()))
        self.test_report = os.path.join(self.test_result_dir, report_name)
        if os.path.exists(self.test_report):
            os.remove(self.test_report)

    def clear_history_log(self):
        """日志目录中只保存最近5次测试日志，删除更早以前的日志文件"""
        log_file_list = os.listdir(self.log_dir)
        log_file_list = sorted(log_file_list, key=lambda x: os.path.getmtime(os.path.join(self.log_dir, x)))
        if len(log_file_list) > Log_Bak_Count:
            for log_file in log_file_list[:-Log_Bak_Count]:
                os.remove(os.path.join(self.log_dir, log_file))

    def clear_history_report(self):
        """报告目录中只保存最近5次测试报告，删除更早以前的报告"""
        report_list = os.listdir(self.test_result_dir)
        report_list = sorted(report_list, key=lambda x: os.path.getmtime(os.path.join(self.test_result_dir, x)))
        if len(report_list) > Report_Bak_Count:
            for report_file in report_list[:-Report_Bak_Count]:
                os.remove(os.path.join(self.test_result_dir, report_file))

    def run_test(self):
        """执行测试用例集"""
        try:
            self.logger.info("************************************测试开始************************************")
            self.generate_report_name()
            if self.test_suite:
                with open(self.test_report, 'wb') as fp:  # 打开测试报告文件，如果不存在就创建
                    runner = HTMLTestRunner(stream=fp, title='Api Test Report', description='Aicall 5.1.3测试环境')
                    runner.run(self.test_suite)
            else:
                self.logger.info("测试集为空，没有需要测试的用例")
        except Exception as e:
            self.logger.error("执行测试用例出现异常,异常信息为: {0}".format(e))
        finally:
            self.logger.info("************************************测试结束************************************")

    def send_report(self):
        mail_body = TextReport(self.test_report).report_content
        log_file = os.path.join(self.log_dir, os.listdir(self.log_dir)[-1])
        self.logger.info("开始发送测试报告...")
        mail_appendix = [self.test_report, log_file]
        SendEmail(mail_body, mail_appendix)


if __name__ == '__main__':
    AllTest()
