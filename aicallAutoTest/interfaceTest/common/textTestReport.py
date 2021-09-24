from bs4 import BeautifulSoup
import re

report_head = """
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Aicall接口测试报告</title>
</head>
<body>
<div height="30px">Hi, all <br> 以下为aicall测试环境接口测试报告，其中pass表示测试用例通过，fail表示测试用例失败，error表示测试用例执行异常，skip表示测试用例未执行。对error或fail的测试用例，可通过查看附件中测试日志定位原因。</div>
"""

report_test_sumary = """ 
<p style="font-weight:bold;font-size:20px">测试概况</p>
<table style="border-collapse:collapse; width: 100%%;">
<tr height="30px">	    
		<td>测试开始时间:</td>
		<td>%(start_time)s</td>		
	</tr>	
	<tr height="30px">
		<td>测试总耗时:</td>
		<td>%(elapse_time)s</td>		
	</tr>	
	<tr height="30px">
		<td>测试结果:</td>
		<td ><font size="3">%(test_sumary)s</font></td>		
	</tr>	
	<tr height="30px">
		<td>测试版本:</td>
		<td>%(test_version)s</td>
	</tr>
	<tr height="30px">
		<td>服务器IP:</td>
		<td>%(server_ip)s</td>		
	</tr>
</table>
"""

report_test_detail = """
<p style="font-weight:bold; font-size:20px">详细测试结果</p>
<table style="border-collapse:collapse; width: 100%%; " border=1>
	<tr style="font-weight:bold; background: #00FFFF">
	    <td width="4%">序号</td>
	    <td width="15%">用例名称</td>
	    <td width="8%">测试结果</td>
		<td width="8%">测试耗时</td>
		<td width="67%">备注信息</td>
	</tr>
"""

report_tail = """
</table>
<p style="font-size:18px">更多详细信息请查看附件！！<a href="http://192.168.180.122">点击访问智能机器人平台</a> </p>

</body>
</html>
"""


class TextReport:
    def __init__(self, report_path):
        self.report_path = report_path
        with open(self.report_path, "rb") as f:
            self.bs = BeautifulSoup(f.read(), "html.parser")

        self.new_report = report_head

        self.get_table_tag()
        self.get_test_sumary()
        self.get_test_detail()
        self.make_sumary_report()
        self.make_detail_report()
        self.report_content = report_head + self.sumary_report + self.detail_report + report_tail

    def get_table_tag(self):
        self.table = self.bs.find_all("table")
        if len(self.table) <= 1:
            exit(0)

    def get_test_sumary(self):
        tr_tags = self.table[0].find_all("tr")
        self.sumary_data = []
        for tr_tag in tr_tags:
            self.sumary_data.append(tr_tag.find_all("td")[1].text)

    def get_test_detail(self):
        result_data = []
        tr_tags = self.table[1].find_all("tr", attrs={'id': re.compile(r"[pefs]t\d+.\d+.\d+")})
        for tr_tag in tr_tags:
            td_value = []
            for td_tag in tr_tag.find_all("td"):
                td_value.append(td_tag.text.strip("\n"))
            result_data.append(td_value)

        self.detail_data = []
        i = 1
        for data in result_data:
            row_data = [data[1], data[3], data[2], data[4]]
            row_data.insert(0, i)
            self.detail_data.append(row_data)
            i += 1

    def make_sumary_report(self):
        elapse_time = self.sumary_data[1].split(":")
        time = int(elapse_time[0]) * 3600 + int(elapse_time[1]) * 60 + float(elapse_time[2])
        self.sumary_report = report_test_sumary % dict(start_time=self.sumary_data[0],
                                                       elapse_time=str(round(time, 2)) + "s",
                                                       test_sumary=self.sumary_data[2],
                                                       test_version=self.sumary_data[3],
                                                       server_ip="192.168.180.122, 192.168.180.129, 192.168.182.81, 192.168.179.27, 192.168.179.28")

    def make_detail_report(self):
        self.detail_report = report_test_detail
        tem_html = """
            <tr>
		        <td>%(id)s</td>
		        <td>%(case_name)s</td>
		        <td style="color:%(color)s">%(result)s</td>
		        <td>%(elapse_time)s</td>
		        <td style="color:%(color)s">%(except_msg)s</td>
	        </tr>
        """
        for data in self.detail_data:
            color = ""
            result = "fail"
            if "pass" in data[2]:
                color = "green"
                result = "pass"
            if "fail" in data[2]:
                color = "red"
                result = "fail"
            if "error" in data[2]:
                color = "fuchsia"
                result = "error"
            if "skip" in data[2]:
                color = "orange"
                result = "skip"

            self.detail_report += tem_html % dict(id=data[0],
                                                  case_name=data[1],
                                                  color=color,
                                                  result=result,
                                                  elapse_time=data[3],
                                                  except_msg="" if data[2] == "pass" else re.findall(":\s(.+)", data[2])[0])


if __name__ == "__main__":
    test_report = "E:/pythtonProject/interfaceTest/result/aicall_test_report_20210407160244.html"
    print(TextReport(test_report).report_content)
