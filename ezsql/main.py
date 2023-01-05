import argparse
from ezsql.cmdline import init_proj,parse_proj,resultcol_proj,example_proj

# 入口函数
def main():
    parser = argparse.ArgumentParser(description="Help you maintain a complex SQL script")

    parser.add_argument('-i','--init', help="Initialize project directory", action="store_true")
    parser.add_argument('-p','--parse', help="Parse the project and get the result SQL script", action="store_true")
    parser.add_argument('-rc','--resultcol', help="Get result column names", action="store_true")
    parser.add_argument('-eg','--example', help="Generate an example of this project", action="store_true")

    args = parser.parse_args()

    if args.init:
        init_proj.init_proj()
    if args.parse:
        parse_proj.parse_proj()
    if args.resultcol:
        resultcol_proj.resultcol_proj()
    if args.example:
        example_proj.example_proj()
    # 如果没有参数传入就输出help
    has_kwargs = False
    for k,v in args._get_kwargs():
        if v:
            has_kwargs = True
            break
    if len(args._get_args())==0 and not has_kwargs:
        parser.print_help()

