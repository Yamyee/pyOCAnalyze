import baseClass
import parse
import re

define = '@interface'
end = '@end'
prop = '@property'


def filterProperty(line):
    if not line.strip(" ").startswith(prop):
        return None
    pro = baseClass.Property()
    pro.modifiers = parse.filterArr(line, "(", ")", ",")
    sep = " "
    if "*" in line:
        sep = "*"
    arr = parse.filterArr(line, ")", ";", sep)
    if len(arr) > 1:
        pro.type = arr[0]
        pro.name = arr[1]
    if 'class' in pro.modifiers:
        pro.isStatic = True
    return pro


def filterParam(line):

    ps = []
    p = baseClass.Param()
    buf = ''
    i = 0
    name = ''
    while i < len(line):
        if line[i] == "(":
            name += buf.strip(" ")
            buf = ''
        elif line[i] == ")":
            p.type = buf.replace("*", "").strip(" ")
            print(p.type)
            buf = ''
        elif line[i] == " " and len(p.type) > 0:
            p.name = buf.strip(" ")
            ps.append(p)
            p = baseClass.Param()
            buf = ''
        else:
            buf += line[i]

        i += 1
    return ps, name


#解析方法声明
def filterMethodDecl(line):
    if not line.startswith('+') and not line.startswith('-'):
        return None
    method = baseClass.Method()
    method.isStatic = True if line.strip(' ').startswith('+') else False
    lis = re.findall('(?<=\\()(.+?)(?=\\))', line, 0)
    if len(lis) == 0:
        return None
    method.returnType = lis[0]
    if ":" not in line:
        method.name = parse.filterContent(line, ")", ";")
        return method
    sp = method.returnType + ")"
    l = line.split(sp)[1]
    params, name = filterParam(l)
    method.params = params
    method.name = name
    return method


def filterClassName(line):
    name = ""
    if ":" in line:
        name = parse.filterContent(line, define, ":")
    elif "(" in line and ")" in line:
        name = parse.filterContent(line, define, "(")

    if name == line:
        return ""
    return name


def filterSuperclass(line):
    if ":" not in line:
        return ""
    arr = line.split(":")
    if len(arr) < 2:
        return ""

    supercls = arr[1]
    if "<" in supercls:
        supercls = supercls.split("<")[0].strip(" ")
    return supercls


def filterProtocols(line):
    if "<" in line:
        pros = parse.filterArr(line, "<", ">", ",")
        return pros
    return []


def parseInterface(content):
    has = False
    interfaces = []
    inter = baseClass.Interface()
    append = ''
    for line in content:
        #@interface开头
        if line.startswith(define):
            inter.name = filterClassName(line)
            inter.superclass = filterSuperclass(line)
            inter.protocols = filterProtocols(line)
            has = True
        #@end 结束
        elif has and line.startswith(end):
            interfaces.append(inter)
            inter = baseClass.Interface()
            has = False
        elif has and line.startswith(prop):
            p = filterProperty(line)
            if not p is None:
                inter.propertys.append(p)
        elif has:
            append += line
            if not append.endswith(';'):
                append += " "
            if (append.startswith("-")
                    or append.startswith("+")) and append.endswith(';'):
                m = filterMethodDecl(append.strip(" "))
                if not m is None:
                    inter.methods.append(m)
                append = ''

    return interfaces