import re
import os

class SQLParser:
    def __init__(self,segment_path):
        # 储存@口径片段
        self.section_map = dict()
        self.result_sql = ""
        self.segment_path = segment_path

    def gen_result_sql(self,sql_str):
        self.result_sql = self.parse_sql(sql_str)

    # DFS解析sql字符串，逻辑是1.递归停止条件为无法划分;2.划分三段left,@{xxx}->递归,right->递归;3.拼接三段
    def parse_sql(self, sql_str):
        rex = re.search("@\{(.+?)\}",sql_str)
        # 1.无法划分，停止递归并返回字符串
        if rex is None:
            return sql_str
        # 2.划分三段
        l,r = rex.span()
        left = sql_str[:l]
        mid = rex.group(1)
        right = sql_str[r:]
        # 2.1.划分三段:处理中段
        # 从参数里解析出tag,spaces,alias三个参数
        params_str = rex.group(1)
        args = self.parse_params(params_str)
        tag = args[0]
        spaces = " "*int(args[1])
        if len(args)<=2:
            alias = 'true'
        else:
            alias = args[2]
        # lazy模式拼接sql
        if tag in self.section_map:
            at_text = self.section_map[tag]
        else:
            file_path = os.path.join(self.segment_path,"{}.sql".format(tag))
            at_text = self.get_sql(file_path)
            # 递归获取at_text
            at_text = self.parse_sql(at_text) # dfs解析at_text
            self.section_map[tag] = at_text
        
        # 判断一下是不是要去掉别名，是不是要apply一个pattern
        if alias.lower() == 'false':
            at_text = re.sub("as\s+\w+\s*(?=--|\n|$)","",at_text).strip()
        elif re.search("^apply\(.+\)$",alias) is not None:
            pattern_str = re.search("^apply\((.+)\)$",alias).group(1)
            at_text = self.apply_to_cols(at_text,pattern_str)
        # 给每行加上指定的空格数
        at_text = at_text.replace("\n","\n"+spaces).strip()
        mid = at_text
        # 2.2.划分三段:处理右段
        right = self.parse_sql(right) # dfs解析right
        # 3.拼接左中右三段sql
        return left + mid + right

    # 返回sql_str
    def get_sql(self,file_path):
        with open(file_path,"r",encoding="utf-8") as f:
            text = f.read()
            rex = re.search("\(body\)((?:.|\n)+)--.*\(/body\)",text)
            if rex is None:
                return None
            sql_str =  rex.group(1)
            return sql_str.strip()

    # 把样式应用到多个列||pattern_str like "sum([body]) as [alias]_d"
    def apply_to_cols(self,cols_str,pattern_str):
        col_collector = []
        brackets = 0  # 括号计数
        quots = 0  # 引号计数
        col_num = 0 # 字段计数
        l = 0
        for r,c in enumerate(cols_str):
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
                col_str = re.sub("(--.+$)|(--.+\n)"," ",cols_str[l:r]).strip()  # 去掉注释
                rex_as = re.search("(.+?)\s+as\s+(\w+)$",col_str)  # 有as的情况
                rex_end = re.search("(\w+)$",col_str)      # 没有as的情况
                if rex_as is not None:
                    col_collector.append({
                        "col_alias":rex_as.group(2),
                        "col_body":rex_as.group(1),
                    })
                elif rex_end is not None:
                    col_collector.append({
                        "col_alias":rex_end.group(1),
                        "col_body":col_str,
                    })
                else:
                    col_collector.append({
                        "col_alias":"col_%04d"%col_num,
                        "col_body":col_str,
                    })

                l = r+1
        # 剩下最后一个字段
        col_num += 1
        col_str = re.sub("(--.+$)|(--.+\n)"," ",cols_str[l:]).strip()
        rex_as = re.search("(.+?)\s+as\s+(\w+)$",col_str)  # 有as的情况
        rex_end = re.search("(\w+)$",col_str)      # 没有as的情况
        if rex_as is not None:
            col_collector.append({
                "col_alias":rex_as.group(2),
                "col_body":rex_as.group(1),
            })
        elif rex_end is not None and rex_end.group(1).lower != "end":
            col_collector.append({
                "col_alias":rex_end.group(1),
                "col_body":col_str,
            })
        else:
            col_collector.append({
                "col_alias":"col_%04d"%col_num,
                "col_body":col_str,
            })
        # 重新拼接成SQL
        result_sql = ""
        for col_dic in (col_collector):
            col_str = re.sub("\[body\]",col_dic["col_body"],pattern_str)
            col_str = re.sub("\[alias\]",col_dic["col_alias"],col_str)
            result_sql += col_str + "\n,"
        result_sql = result_sql.strip("\n,")
        return result_sql

    # 解析@{xxxx}参数，返回参数列表
    def parse_params(self,param_str):
        params = []
        brackets = 0  # 括号计数
        quots = 0  # 引号计数
        col_num = 0 # 字段计数
        l = 0
        for r in range(len(param_str)):
            c = param_str[r]
            if quots == 0:
                if c in ["(","["]:
                    brackets += 1
                if c in [")","]"]:
                    brackets -= 1
            if c == "'":
                quots = (quots^1)
            if c == '"':
                single_quots = (quots^2)
            # 括号结清，引号结清的情况下遇到逗号就作为一个字段          
            if brackets == 0 and quots == 0 and c == ",":
                col_num += 1
                params.append(param_str[l:r].strip())
                l = r+1
        # 剩下最后一个字段
        col_num += 1
        params.append(param_str[l:].strip())
        
        return params


        





