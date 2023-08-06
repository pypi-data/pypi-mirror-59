# norepeat

The [norepeat](https://pypi.org/project/norepeat/1.0.0/) package contains some magical function, it's my personal tools collection...

1 Count a project sum of codes number

2 Generate markdown menu automatically


## Installation

You can install the Real Python Feed Reader from [PyPI](https://pypi.org/project/norepeat/):

```
pip install norepeat
```
The norepeat is supported on Python 3 and above.

## DOC
norepeat -h

norepeat gen_markdown_menu -h

norepeat count_code_nums -h

```
count_code_nums
usage: count_code_nums [-h] [-p PATH] [-t TYPE]

    Count summary codes lines/统计代码行数
    Eg:
        norepeat count_code_nums -p=project -t=py


optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  file/directory path
  -t TYPE, --type TYPE  file type
************************************************************
gen_markdown_menu
usage: gen_markdown_menu [-h] [-n NAME]

    Generate markdown Menu automatically/自动生成markdown 目录
    Eg:
        norepeat gen_markdown_menu -n=sample.md
    then you will get a sample_back.md with contents
    sample_back.md is new generated file including menu


optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  file name
************************************************************
rename_file
usage: rename_file [-h] [-d DIR_PATH] [-p PREFIX] [-s SUFFIX] [-r REMOVE]
                   [-i ID]

    Rename multiple file names
    Eg:
        norepeat rename_file -d=test -p=test  -s=end -r=true -i=true
        before:
            dir
                a.txt
                b.txt
        after:
            dir
                testaend1.txt
                testbend1.txt



optional arguments:
  -h, --help            show this help message and exit
  -d DIR_PATH, --dir_path DIR_PATH
                        directory path
  -p PREFIX, --prefix PREFIX
                        new file name prefix
  -s SUFFIX, --suffix SUFFIX
                        new file name suffix
  -r REMOVE, --remove REMOVE
                        new file name with removing src name
  -i ID, --id ID        new file name need id
************************************************************

```

## norepeat package (Private)
https://pypi.org/project/norepeat/1.0.0/

TEST:
* python3 setup.py sdist bdist_wheel
* python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

PROD:

* python3 setup.py sdist bdist_wheel

* twine upload dist/*
