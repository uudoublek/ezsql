import os
from ezsql.utils.parse_sql import SQLParser

def parse_proj():
    # 获取当前工作路径
    path_cwd = os.getcwd()
    main_sql_path = os.path.join(path_cwd,"result","main.sql")
    segments_path = os.path.join(path_cwd,"segments")
    result_sql_path = os.path.join(path_cwd,"result","result.sql")
    if not check_path(path_cwd):
        print("Unable to resolve project!")
        return
    # 获取main.sql
    sql_str = get_sql_str(main_sql_path)
    # 解析sql语句
    parser = SQLParser(segments_path)
    parser.gen_result_sql(sql_str)
    # 输出结果语句
    with open(result_sql_path,"w",encoding="utf-8") as f:
        f.write(parser.result_sql)

# 获取sql语句
def get_sql_str(sql_path):
    sql_str = ""
    with open(sql_path,"r",encoding="utf-8") as f:
        sql_str = f.read()
    return sql_str

# 路径检查下是否至少已经完成初始化
def check_path(path):
    # 获取当前工作路径
    segments_path = os.path.join(path,"segments")
    result_path = os.path.join(path,"result")
    main_sql_path = os.path.join(path,"result","main.sql")
    # 检查路径下的文件夹是否已经存在
    if not os.path.exists(segments_path):
        print("Folder segments is missing, please initialize the project")
        return False
    if not os.path.exists(result_path):
        print("Folder result is missing, please initialize the project")
        return False
    if not os.path.exists(main_sql_path):
        print("File main.sql is missing, please initialize the project")
        return False
    return True