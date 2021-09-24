import json
import yaml


def read_yaml(yaml_path):
    """读取yaml格式文件,返回字典数据结构内容"""
    f = open(yaml_path, 'r', encoding='utf-8')
    cont = f.read()
    yaml_content = yaml.load(cont)
    f.close()
    return yaml_content


def parse_json(json_string):
    """解析JSON格式字符串，返回字典数据结构"""
    try:
        return json.loads(json_string)
    except ValueError as e:
        raise ValueError("Could not parse '%s' as JSON: %s" % (json_string, e))


def stringify_dic(dic_data):
    """将字典数据结构转换为JSON格式字符串"""
    try:
        return json.dumps(dic_data, ensure_ascii=False)
    except ValueError as e:
        raise ValueError("Could not stringify '%r' to JSON: %s" % (dic_data, e))


def get_url(server_ip, port, path):
    """将服务器IP、端口、路径拼接成完整url"""
    return "http://{0}:{1}/{2}".format(server_ip, port, path.strip("/"))

