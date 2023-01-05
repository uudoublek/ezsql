import os
from ezsql.utils.get_result_cols import get_result_cols

def resultcol_proj():
    # 获取当前工作路径
    path_cwd = os.getcwd()
    result_sql_path = os.path.join(path_cwd,"result","result.sql")
    result_cols_path = os.path.join(path_cwd,"result","result_cols.sql")
    if not os.path.exists(result_sql_path):
        print("File main.sql is missing, please initialize the project")
        return
    # 获取结果sql的输出字段名
    col_names = get_result_cols(result_sql_path)
    with open(result_cols_path,"w",encoding="utf-8") as f:
        for col in col_names:
            f.write(col+"\n")