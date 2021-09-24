# -*- coding: gbk -*-
import time
from datetime import datetime
import os
import codecs
import math


# def sqrt(x):
#     y = 1.0
#     while abs(y * y - x) > 1e-6:
#         y = (y + x/y) / 2
#     return y
#
# # name = "name_3pa_____lue_ple_kip_ec________etion_____blue_pple_skip_exception________blue_pele_skip_exception_______blue_pele_skip_ection___qwrtyu_jkbkl_fm________ndkg_rite_be_pple_te_be_peple___________write_blue_peple_rnweqw_write_blue_pe_____lblue_peple_name"
# # head = "name,phone,AggregateAmount,tailnumber,sex,MinAmount,BillingDay"
# # f_path = "E:/项目资料/兴业银行/压测/test.csv"
# # if os.path.exists(f_path):
# #     os.remove(f_path)
# # with codecs.open(f_path, "a", encoding='gbk') as f:
# #     phone = 13071400000
# #     f.write(head + "\n")
# #     for i in range(99999, 199999):
# #         phone += 1
# #         str0 = "%s,%s,32200,%s,先生,200,2021-12-12" % (name, phone, i)
# #         f.write(str0 + "\n")
# # f.close()
#
#
# current_dir = os.path.dirname(__file__)
# log_dir = os.path.join(current_dir, "log").replace("\\", "/")
#
#
# def func():
#     log_file_list = os.listdir(log_dir)
#     lamda = lambda x: os.path.getmtime(os.path.join(log_dir, x))
#     log_file_list = sorted(log_file_list, key=lamda)
#
#
# func()

def sqrt(k):
    x = 10
    print(x - (x / 2 + k / (2*x)))
    while x * x - k > 0.00001 or x * x - k < -0.00001:
        print(x - (x/2 + k/x))
        x = x/2 + k/(2*x)
    return x


x, y = 0, 0
for y in range(1, 18127902):
    x = (18127902 - 15*y)*1.0/12
    if x < 0:
        break
    x_int = math.floor(x)
    if not(x - x_int):
        print("x:{0}, y:{1}".format(x, y))























