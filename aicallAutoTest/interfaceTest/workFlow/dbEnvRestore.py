from common.opmysql import OpMysql


class OpAimatrix:
    def __init__(self, db_ip, db_port, db_user, db_pwd, db_name):
        self.db_conn = OpMysql(db_host=db_ip, db_port=db_port, visit_user=db_user, visit_pwd=db_pwd, db_name=db_name)

    def del_task(self, task_id):
        # 删除
        self.db_conn.op_sql("delete from aicall_task where task_id='{0}'".format(task_id))

    def pause_task(self, task_id):
        # 暂停任务
        self.db_conn.op_sql("update aicall_task set status=5 where task_id='{0}'".format(task_id))

    def start_task(self, task_id):
        # 启动任务
        self.db_conn.op_sql("update aicall_task set status=1 where task_id='{0}'".format(task_id))

    def finish_task(self, task_id):
        # 完成任务
        self.db_conn.op_sql("update aicall_task set status=2 where task_id='{0}'".format(task_id))

    def terminate_task(self, task_id):
        # 终止任务
        self.db_conn.op_sql("update aicall_task set status=3 where task_id='{0}'".format(task_id))

    def query_task_status(self, task_id):
        # 查询任务状态
        return self.db_conn.select_one("select status from aicall_task where task_id='{0}'".format(task_id))[0]

    def del_custom(self, phone):
        # 删除客户资料
        self.db_conn.op_sql("delete from aicall_crm where phone='{0}'".format(phone))

    def del_speech_engine(self, bot_id):
        # 删除语音引擎
        self.db_conn.op_sql("delete from aicall_speech_engine where bot_id='{0}'".format(bot_id))

    def cancel_bind_speech_engine(self, bot_id):
        # 取消语音引擎绑定
        self.db_conn.op_sql("update aicall_speech_engine set asr=0, asr_id=Null, tts_id=Null where bot_id='{0}'".format(bot_id))

    def disconnect(self):
        self.db_conn.close_db_conn()


class OpAibot:
    def __init__(self, db_ip, db_port, db_user, db_pwd, db_name):
        self.db_conn = OpMysql(db_host=db_ip, db_port=db_port, visit_user=db_user, visit_pwd=db_pwd, db_name=db_name)

    def del_bot(self, bot_id):
        # 删除机器人
        self.db_conn.op_sql("delete from aicall_bot where bot_id='{0}'".format(bot_id))
        # 删除机器人对应流程
        self.db_conn.op_sql("delete from aicall_flow where bot_id='{0}'".format(bot_id))
        # 删除机器人对应模型
        self.db_conn.op_sql("delete from aicall_model_bot where bot_id='{0}'".format(bot_id))
        # 删除模型绑定
        self.db_conn.op_sql("delete from aicall_model_bind where bot_id='{0}'".format(bot_id))

    def get_bot_status(self, bot_id):
        return self.db_conn.select_one("select status from aicall_bot where bot_id='{0}'".format(bot_id))[0]

    def del_flow(self, flow_id):
        # 删除机器人流程
        self.db_conn.op_sql("delete from aicall_flow where flow_id='{0}'".format(flow_id))

    def del_entity(self, entity_id):
        # 删除实体
        self.db_conn.op_sql("delete from aicall_entity where ID='{0}'".format(entity_id))
        # 删除正则
        self.db_conn.op_sql("delete from aicall_regx where relation_id='{0}'".format(entity_id))

    def del_intent(self, intent_id):
        # 删除意图
        self.db_conn.op_sql("delete from aicall_intention where ID='{0}'".format(intent_id))
        # 删除正则
        self.db_conn.op_sql("delete from aicall_regx where relation_id='{0}'".format(intent_id))
        # 删除相似问
        self.db_conn.op_sql("delete from aicall_intention_similar where intent_id='{0}'".format(intent_id))
        # 删除填槽
        self.db_conn.op_sql("delete from aicall_intention_similar_slot where intent_id='{0}'".format(intent_id))

    def query_tag_id(self, bot_id, tag_name):
        # 获取标签ID
        return self.db_conn.select_one("select ID from aicall_tag where bot_id='{0}' and tag_name='{1}'".format(bot_id, tag_name))[0]

    def del_tag(self, tag_id):
        # 删除标签
        self.db_conn.op_sql("delete from aicall_tag where ID='{0}'".format(tag_id))

    def del_blue_dot(self, bot_id, intent_name):
        # 删除小蓝点意图
        self.db_conn.op_sql("delete from aicall_bot_trigger where bot_id='{0}' and intent_name='{1}'".format(bot_id, intent_name))

    def del_bot_model(self, bot_id):
        # 删除和机器人绑定的模型数据(包括算法)
        self.db_conn.op_sql("delete from aicall_model_bind where bot_id='{0}'".format(bot_id))
        self.db_conn.op_sql("delete from aicall_model_bot where bot_id='{0}'".format(bot_id))

    def bot_off_line(self, bot_id):
        # 下线机器人
        self.db_conn.op_sql("update aicall_bot set status=0 where bot_id='{0}'".format(bot_id))

    def bot_on_line(self, bot_id):
        # 上线机器人
        self.db_conn.op_sql("update aicall_bot set status=1 where bot_id='{0}'".format(bot_id))

    def query_bot(self, bot_id):
        # 查询机器人数据
        return self.db_conn.select_one("select * from aicall_bot where bot_id='{0}'".format(bot_id))

    def query_flow(self, flow_id):
        # 查询流程数据
        return self.db_conn.select_one("select * from aicall_flow where flow_id='{0}'".format(flow_id))

    def clean_flow_data(self, flow_id):
        # 清理流程数据
        self.db_conn.op_sql("update aicall_flow set flow_dst_data=Null, flow_src_data=Null, flow_type=0 where flow_id='{0}'".format(flow_id))

    def disconnect(self):
        self.db_conn.close_db_conn()

