import baseClass
import parse

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


#解析方法声明
def filterMethodsDecl(line):
    if not line.strip(' ').startswith('+') or not line.strip(' ').startswith(
            '-'):
        return None
    method = baseClass.Method()
    method.isStatic = True if line.strip(' ').startswith('+') else False


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
    for line in content:
        #@interface开头
        if line.startswith(define):
            inter.name = filterClassName(line)
            inter.superclass = filterSuperclass(line)
            inter.protocols = filterProtocols(line)
            has = True
        #@end 结束
        if has and line.startswith(end):
            interfaces.append(inter)
            inter = baseClass.Interface()
            has = False
        if has and line.startswith(prop):
            p = filterProperty(line)
            if not p is None:
                inter.propertys.append(p)

    return interfaces