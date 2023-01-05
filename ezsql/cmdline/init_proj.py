import os

def init_proj():
    done = False
    # 获取当前工作路径
    path_cwd = os.getcwd()
    segments_path = os.path.join(path_cwd,"segments")
    result_path = os.path.join(path_cwd,"result")
    main_sql_path = os.path.join(path_cwd,"result","main.sql")
    # 检查路径下的文件夹是否已经存在
    if not os.path.exists(segments_path):
        os.mkdir(segments_path)
        done = True
    if not os.path.exists(result_path):
        os.mkdir(result_path)
        done = True
    if not os.path.exists(main_sql_path):
        with open(main_sql_path,"w",encoding='utf-8') as f:
            f.write(
'''/*
the main sql file of this project
you can write your main logic here
/*'''
            )
        done = True
    # 汇报结果
    if done:
        print("Initialization has been completed")
    else:
        print("The project does not need to be initialized")
    
    

