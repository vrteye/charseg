import os
from dotenv import load_dotenv
import json

env = "loc"  # 可以改为 "loc", "pro", "dev" 等

# 获取当前文件所在的目录
current_directory = os.path.dirname(__file__)

# 拼接 .env 文件的路径
dotenv_path = os.path.join(current_directory, f'.{env}')

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path)

# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.abspath(__file__))
print(os.environ.get("ENV"))

# 根据需要选择配置文件
config_filename = f"{env}.json"

# 构建跨平台的配置文件路径
config_path = os.path.join(project_root, config_filename)

# 读取配置文件
with open(config_path, 'r', encoding='utf8') as config_file:
    config = json.load(config_file)

# 从环境变量中获取 MySQL 配置信息
mysql_config = {
    "host": os.environ.get(config['mysql']['host']),
    "user": os.environ.get(config['mysql']['user']),
    "password": os.environ.get(config['mysql']['password']),
    "database": os.environ.get(config['mysql']['database']),
    "post": os.environ.get(config['mysql']['post'])
}

mysql_info = [mysql_config['host'], mysql_config['user'], mysql_config['password'], mysql_config['database'],
              int(mysql_config['post'])]

