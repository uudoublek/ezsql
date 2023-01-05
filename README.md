# EZSQL

## Introuction

Ezsql is a command line tool for easy management of long sql scripts. 

## Usage

```shell
% ezsql
usage: ezsql [-h] [-i] [-p] [-rc] [-eg]

Help you maintain a complex SQL script

optional arguments:
  -h, --help        show this help message and exit
  -i, --init        Initialize project directory
  -p, --parse       Parse the project and get the result SQL script
  -rc, --resultcol  Get result column names
  -eg, --example    Generate an example of this project
```

## Tutorial

Step1: Create a new folder named `extract_some_data` 

Step2: Use `ezsql -eg` generate an example of this project.

```sh
.
├── result
│   └── main.sql
└── segments
    └── dim.sql
```

The following  is in `main.sql`

```sql
insert into xxx
select
    @{dim,4,apply([body] as [alias]_new)}
from table
```

The @ {} symbol is used here to refer to a large amount of code, so as to make the code cleaner.

> Note：@{} can also appear in the files of segments, and the parameters can be resolved iteratively.

@{file_name, spaces_num, apply_func}

The `@{}` symbol contains three parameters. **Parameter 1** indicates the file name for replacing this code, which refers to the dim.sql in the segments folder

```sql
-- (body)
name
,age
,gender
,height
,weight
-- (/body)
```

Only the part between `-- (body) `and`-- (/body)` will be replaced as the body, and other places can be freely written with some comments.

**Parameter 2 ** is used to specify the number of indented spaces in this section of SQL. This is to allow developers to ensure the beauty of the code.

**Parameter 3 ** is similar to an apply function. It will process all fields in dim.sql in the same way. In some cases, this can save a lot of repetitive work. There are two reserved symbols [body] and [alias], which represent the field and its alias respectively.

Step3: Execute `ezsql -p`, and we will get a result.sql file

```sh
.
├── result
│   ├── main.sql
│   └── result.sql
└── segments
    └── dim.sql
```

The following  is in `result.sql`

```sh
insert into xxx
select
    name as name_new
    ,age as age_new
    ,gender as gender_new
    ,height as height_new
    ,weight as weight_new
from table
```

This is the script we finally get.

This is just a simple example. The tool can be used flexibly, and can help users easily maintain a super long SQL scripts with more than thousand lines.