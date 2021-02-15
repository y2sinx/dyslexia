import re
from dyslexia import common
from dyslexia import NEEDED_PATH
from collections import defaultdict

# ht文件的结构及注意事项
EXPLANATION = """
ht文件是Python双层字典(内层键的值是一个序列)的一种文本形式.
一个ht行应该与一个外层字典的键值对一一对应:

字典值: 'head': {'tag_1': ['T11', 'T12', '...', 'T1n'], 
                'tag_2': ['T21', 'T22', '...', 'T2n'],
                '...',
                'tag_m': ['Tm1', 'Tm2', '...', 'Tmn']}
信息行: head % [tag_1]T11;T12;...;T1n; [tag_2]T21;T22;...;T2n; ..., [tag_m]Tm1;Tm2;...;Tmn;
    

说明
===
1) ht文件以行为基本单元,分为注释行和信息行两种;
2) 信息行是以数字或字母开始,并且含有分隔符(%)的行;所有的非信息行都是注释行;
3) 信息行的结构一致分为 头部,分隔符(%),尾部,为便于可读性,其使用空格分隔;
4) 在尾部中,`[`与`]`所夹的内容为行标签(亦即Python内层字典的键);
5) 当前标签后的`]`与下一个标签前的`[`所夹的内容(为了可读性,`[`可以含有空格)为当前标签的值(末尾标签除外),每个值均通过`;`分割;
6) 尾部中可能存在`<>`,表示伪标签,用于强调或者辅助索引等.
7) ht行的特殊符号有四个: `%`,`[`,`]`,`;`,这四个符号的用法一定不能出错.
8) 在ht文件中,每个ht行有且仅有一个位于末尾的换行符`\n`.
9) 当ht文件中的行只有头部而没有分隔符和尾部时,若想要获取所有的头部,可以以`\n`为分隔符.

+) 纯单词行也是信息行;
                                     
"""


def is_inf_line(line, sep="%"):
    """判断行是不是信息行: 首字符为字母或数字,且以sep为分隔符."""

    return line.strip() != "" and line[0].isalnum() and sep in line


def split_line(line, sep="%"):
    """使用分隔符分割ht行;
    当sep='\n'时表示分割纯单词行."""

    if is_inf_line(line, sep):
        if sep == "\n":
            head, _ = line.split("\n")
            tail = "我是纯单词行的虚拟尾巴!"  ##将纯单词行的行尾由''改为'0'
        else:
            line = line.strip("\n")  ##需要换行符的时候自己添加
            p = line.find(sep)
            head, tail = line[:p].strip(), line[p + 1 :].strip()

    else:  ##分割注释行,空行会被当做注释行
        try:
            head, _ = line.split("\n")
            tail = "我是注释行!"  ##将注释行的行尾由''改为'#'
        except:
            head, tail = line, None  # 读取纯单词行词表的最后一行时,其行尾没有换行符
    return head, tail


def tail_to_dict(head, tail, check_tag=False):
    """将tail转化为一个内层字典."""

    inner = defaultdict(list)
    if "[" not in tail:  ##行中没有标签时添加默认标签[x]
        inner = {"x": [tail]}  ##内层字典的值必须为列表

    else:  ##tail中有标签

        tails = tail.split("[")

        bc = tails[0].strip()  ##判断第一个`[`前是否含有字符串,若有,为其添加默认标签[x]并保存,否则将会丢失其内容.
        if bc != "":
            inner["x"] = [bc]  ##内层字典的值必须为列表

        for tag_values in tails[1:]:  ##['tag1]:values;','tag2]:values']
            p = tag_values.find("]")  ##查找tag结束的位置
            tag = tag_values[:p]  ##获取tag名
            values = (
                tag_values[p + 1 :].strip().split(";")
            )  ##获取tag所对应的值列表:`值1;值2;`=>[值1,值2]

            if check_tag and tag in inner.keys():
                print("{} # repeated [{}]!".format(head, tag))

            for value in values:
                if value not in inner[tag]:  ##默认字典可以取不存在的键
                    inner[tag].append(value)  # 一个值一个值的添加

            while "" in inner[tag]:  # 删除tag的值列表中的所有空串
                inner[tag].remove("")

    return dict(inner)


def line_to_dict(line, sep="%", check_tag=False):
    """将ht条目行转化为字典;"""

    outer = {}  ##外层字典: `head: tail`
    inner = {}  ##内层字典: `tag: values`

    head, tail = split_line(line, sep)  ##可以同时分割注释行和信息行

    if tail == "#":  ##这是注释行
        outer[head] = {"#": [""]}  ##保证内层字典的值为列表
    elif tail == "0":  ##这是纯单词行
        outer[head] = {"0": [""]}
    else:  ##包含tag的信息行
        inner = tail_to_dict(head, tail, check_tag)
        outer[head] = inner
    return outer


def ht_to_dict(file, sep="%", check_tag=False):
    """将文本文件转化为字典"""
    dn = {}
    with open(file, "r", encoding="utf-8") as fp:
        for line in fp:
            dn.update(line_to_dict(line, sep, check_tag))  # 若有重复单词,添加的是后面的含义
    return dn


def print_line(line, sep="%"):
    """分行显示一个HT信息行."""
    if is_inf_line(line, sep):
        head, tail = split_line(line, sep)
        head = head + " " + sep + "\n" + "-" * 32
        tail = tail.replace("[", "\n[").replace("]", "]: ")
        line = head + tail
        print(line)


def line_sorted(file, overwrite=True):
    """将单词本中的词条按字母顺序排序."""
    if not overwrite:  ##创建一个新的文件
        file2 = file + ".sort"
    else:
        common.backup(file, "sort")  ##覆盖源文件
        file2 = file

    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        sorted_lines = sorted(set(lines))

    with open(file2, "w", encoding="utf-8") as f2:
        for line in sorted_lines:
            if line.strip() != "\n":
                f2.write(line)
    return file2


def get_repeated_heads(file, sep="%"):
    """获取文件中所有重复的head及其重复的次数"""
    heads = []
    with open(file, "r", encoding="utf-8") as fp:
        for line in fp:
            head = split_line(line, sep=sep)[0]
            heads.append(head)
    dn = defaultdict(int)
    for head in heads:
        dn[head] = dn[head] + 1
    out = []
    for k, v in dn.items():
        if v > 1:
            out.append((k, v))
    return sorted(out)


def get_comments(file, sep="%"):
    """打印ht文件中的所有注释."""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if not is_inf_line(line, sep):
                print(line.strip("\n"))


def union(f1, f2, use_f2=False, overwrite=True):
    """将第二个文件合并到第一个;
    不要使用<合并EnDict字典后导出:主要用于整理格式>的方式: 太慢."""

    with open(f1, "r", encoding="utf-8") as fp1:
        lines1 = fp1.readlines()
    with open(f2, "r", encoding="utf-8") as fp2:
        lines2 = fp2.readlines()

    dn1 = {}
    for line in lines1:
        head, tail = split_line(line)
        dn1[head] = line

    dn2 = {}
    for line in lines2:
        head, tail = split_line(line)
        dn2[head] = line

    head1 = dn1.keys()
    head2 = dn2.keys()
    heads = set(sorted(head1) + sorted(head2))

    lines = []
    for head in sorted(heads):
        if use_f2:
            if head in head2:
                lines.append(dn2[head])
            else:
                lines.append(dn1[head])

        else:
            if head in head1:
                lines.append(dn1[head])
            else:
                lines.append(dn2[head])
    if overwrite:
        common.backup(f1, "plus_f2")
        f3 = f1
    else:
        f3 = f1 + ".union"
    with open(f3, "w", encoding="utf-8") as fp3:
        fp3.writelines(sorted(lines))  # 自动添加'\n'?
    return f3


def tan(ptn, file_or_key, flag_print_ht=True, sep="%", emphasize="✅"):
    """search的ht版本."""
    try:
        file = NEEDED_PATH[file_or_key]
    except:
        file = file_or_key

    with open(file, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
    heads = []
    for i, line in enumerate(lines):
        mat = re.findall(ptn, line)
        if mat != []:
            head, _ = split_line(line, sep=sep)
            heads.append(head)
            line = line.replace(
                mat[0], "{}{}{}".format(emphasize, mat[0], emphasize), 1
            )
            if flag_print_ht:
                # print_line(line, sep=sep)  # bug,行首添加前调符之后无法打印
                print(line,end='')
    if not flag_print_ht:
        return sorted(set(heads))
