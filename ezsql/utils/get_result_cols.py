import re

# 获取输出字段名
def get_result_cols(sql_path):
    result_sql = ""
    with open (sql_path,"r",encoding="utf-8") as f:
        result_sql = f.read()
    rex = re.search("insert(?:.|\n)+?select((?:.|\n)+?)from",result_sql,flags=re.IGNORECASE)
    if rex is None:
        print("result_sql格式有误")
        return
    sql_str = rex.group(1).strip()
    
    col_collector = []
    brackets = 0  # 括号计数
    quots = 0  # 引号计数
    col_num = 0 # 字段计数
    l = 0
    for r,c in enumerate(sql_str):
        if quots == 0:
            if c in ["(","[","{"]:
                brackets += 1
            if c in [")","]","}"]:
                brackets -= 1
        if c == "'":
            quots = (quots^1)
        if c == '"':
            single_quots = (quots^2)
        # 括号结清，引号结清的情况下遇到逗号就作为一个字段          
        if brackets == 0 and quots == 0 and c == ",":
            col_num += 1
            col_logic = re.sub("(--.+$)|(--.+\n)"," ",sql_str[l:r]).strip()  # 去掉注释
            rex_as = re.search("as\s+(\w+)$",col_logic)  # 有as的情况
            rex_end = re.search("(\w+)$",col_logic)      # 没有as的情况
            if rex_as is not None:
                col_collector.append(rex_as.group(1))
            elif rex_end is not None and rex_end.group(1).lower != "end":
                col_collector.append(rex_end.group(1))
            else:
                col_collector.append("col_%04d"%col_num)

            l = r+1
    # 剩下最后一个字段
    col_num += 1
    col_logic = re.sub("(--.+$)|(--.+\n)"," ",sql_str[l:]).strip()
    rex_as = re.search("as\s+(\w+)$",col_logic)  # 有as的情况
    rex_end = re.search("(\w+)$",col_logic)      # 没有as的情况
    if rex_as is not None:
        col_collector.append(rex_as.group(1))
    elif rex_end is not None and rex_end.group(1).lower != "end":
        col_collector.append(rex_end.group(1))
    else:
        col_collector.append("col_%04d"%col_num)
    # 输出总行数并返回字段名
    print("===== total col num is %d ======"%col_num)
    return col_collector

