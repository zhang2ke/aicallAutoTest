from configobj import ConfigObj
import os

conf_ini = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.ini")
cf = ConfigObj(os.path.abspath(conf_ini))


class ConfigInfo(object):
    def __init__(self):
        self.email_switch = cf["email_info"]["on_off"]
        self.email_host = cf["email_info"]["host"]
        self.email_sender = cf["email_info"]["sender"]
        self.email_pwd = cf["email_info"]["pwd"]
        self.email_receivers = cf["email_info"]["receivers"] if isinstance(cf["email_info"]["receivers"], list) else [cf["email_info"]["receivers"]]
        self.email_subject = cf["email_info"]["subject"]

        self.log_name = cf["log_info"]["name"]
        self.log_file_level = cf["log_info"]["file_level"]
        self.log_console_level = cf["log_info"]["console_level"]
        self.log_bak_count = cf["log_info"]["bak_count"]

        self.report_bak_count = cf["report_info"]["bak_count"]

    def get_email_info(self):
        return {"email_switch": self.email_switch,
                "sender": self.email_sender,
                "pwd": self.email_pwd,
                "receivers": self.email_receivers,
                "subject": self.email_subject,
                "host": self.email_host,
                }

    def get_log_info(self):
        return {"name": self.log_name,
                "file_level": self.log_file_level,
                "console_level": self.log_console_level,
                "bak_count": self.log_bak_count,
                }


if __name__ == "__main__":
    t = ConfigInfo().get_email_info()
    print(t)
