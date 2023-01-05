import os
from ezsql.cmdline import init_proj


def example_proj():
    # print(os.path.abspath(__file__))
    # 获取当前工作路径
    path_cwd = os.getcwd()
    segments_path = os.path.join(path_cwd,"segments")
    result_path = os.path.join(path_cwd,"result")
    main_sql_path = os.path.join(result_path,"main.sql")
    dims_sql_path = os.path.join(segments_path,"dim.sql")
    if os.path.exists(main_sql_path) or os.path.exists(dims_sql_path):
        print("Your project has been initialized!")
        return
    init_proj.init_proj()
    # 写入样例
    with open(main_sql_path,'w',encoding='utf-8') as f:
        f.write(
'''insert into xxx
select
    @{dim,4,apply([body] as [alias]_new)}
from table
'''
        )
    with open(dims_sql_path,'w',encoding='utf-8') as f:
        f.write(
'''
-- (body)
name
,age
,gender
,height
,weight
-- (/body)
'''
        )
    # 提示
    print("Now you can use 'ezsql -p' to get the resutl.sqls")