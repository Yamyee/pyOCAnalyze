import types
import baseClass
import parse
import re

define = '@interface'
end = '@end'
prop = '@property'
methodEnds = ["{",";","__attribute__","//"]

def filterPropertyTypeName(line):
    type = ''
    name = ''
    i = 0
    buf = ''
    arr = []
    while i < len(line):
        if line[i] == ')' and "^" in buf and ")" in buf:
            buf += line[i]
            type = buf
            name = parse.filterContent(type,"^",")")
            type = type.replace(name,"")
            break
        elif line[i] == '*' and '^' not in buf:
            type += line[i]
            buf = ''
        elif line[i] == ' ' and len(buf) > 0 and len(type) == 0 and '^' not in buf:
            type = buf
            buf = ''
        elif len(type) > 0 and line[i] in methodEnds:
            name = buf
            break
        elif not line[i] == ' ':
            buf += line[i]
        i += 1
    return type,name

allModifier = ['strong','weak','assing','class','unsafe_unretained','retain','copy','nonatomic','readwrite','readonly','writeonly','null_resettable']
def filterModifiers(line):
    i = 0
    res = []
    arr = []
    buf = ''
    while i < len(line):
        if line[i] == "(":
            buf = ''
            arr.append(line[i])

        elif line[i] == ")" and arr[-1] == "(":
            del arr[-1]
            if len(arr) == 0:
                if buf in allModifier:
                    res.append(buf)
                break
        elif len(arr) > 0 :
            if line[i] == ',' or line[i] == ' ':
                if buf in allModifier:
                    res.append(buf)
                buf = ''
            else:
                buf += line[i]
        i += 1
    return res,i

def filterProperty(line):
    if not line.strip(" ").startswith(prop):
        return None
    pro = baseClass.Property()
    modifiers,i = filterModifiers(line)
    pro.modifiers = modifiers
    l = line[i+1:]
    type,name = filterPropertyTypeName(l)
    pro.type = type
    pro.name = name
    return pro


def filterParam(line):

    ps = []
    p = baseClass.Param()
    buf = ''
    i = 0
    name = ''
    arr = []
    while i < len(line):
        if line[i] == ":":
            #一段方法名
            buf += line[i]
            name += buf.strip(" ")
            buf = ''
            i += 1
            continue

        if not line[i] == ' ':
            buf += line[i]
        
        if line[i] == "(": 
            arr.append(line[i])#入栈
        elif line[i] == ")" and arr[-1] == "(":
            del arr[-1] #出栈
            if len(arr) == 0:
                p.type = buf[1:][:-1] #参数类型
                buf = ''
        elif line[i] == " " and len(p.type) > 0:
            p.name = buf #参数名
            ps.append(p)
            p = baseClass.Param()
            buf = ''

        i += 1
    return ps, name

seps = [" ","{","\n","\t"]
def filterPureName(line):
    i = 0
    name = ''
    while i < len(line):
        if line[i] == ' ':
            if name == '':
                i += 1
                continue
            else:
                break
        elif line[i] not in seps:
            name += line[i]
        else:
            break

        i += 1
    return name

def filterReturnType(line):
    if len(line)==0:
        return 0,''
    arr = []
    do = True
    buf = ''
    i = 0
    while do and i < len(line):
        if line[i] == '+' or line[i] == '-':
            i += 1
            continue
        if line[i] == ' ' and len(arr) == 0:
            i += 1
            continue
        if line[i] == '(':
            arr.append(line[i])
        elif line[i] == ')' and arr[-1] == '(':
            del arr[-1]
        if not line[i] == ' ':
            buf += line[i]
        if i > 0 and len(arr) == 0:
            do = False
        i += 1
    return i,buf

#解析方法声明
def filterMethodDecl(line):
    if not line.startswith('+') and not line.startswith('-'):
        return None
    method = baseClass.Method()
    method.isStatic = True if line.strip(' ').startswith('+') else False
    i,returnType = filterReturnType(line)
    returnType = returnType[1:][:-1]
    method.returnType = returnType
    l = line[i:]
    if ':' in l:
        params, name = filterParam(l)
        method.params = params
        method.name = name
    else:
        method.name = filterPureName(l)
    if len(method.name) == 0:
        return None
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

def filterCategory(line):
    lis = re.findall('(?<=\\()(.+?)(?=\\))', line, 0)
    if len(lis)==0:
        return ''
    return lis[0]

def filterProtocols(line):
    if "<" in line:
        pros = parse.filterArr(line, "<", ">", ",")
        return pros
    return []


def parseInterface(content):
    has = False
    interfaces = []
    propertys = []
    append = ''
    for line in content:
        #@interface开头
        if line.startswith(define):
            name = filterClassName(line)
            superclass = filterSuperclass(line)
            protocols = filterProtocols(line)
            cat = filterCategory(line)
            if len(cat)>0:
                name += "({})".format(cat)
            has = True
        #@end 结束
        elif has and line.startswith(end):
            inter = baseClass.Interface()
            inter.name = name
            inter.superclass = superclass
            inter.protocols = protocols
            inter.propertys = propertys
            interfaces.append(inter)
            propertys = []
            has = False
        elif has and line.startswith(prop):
            p = filterProperty(line)
            if not p is None:
                propertys.append(p)
        #暂时不解析方法声明
        # elif has:
        #     append += line
        #     if not append.endswith(';'):
        #         append += " "
        #     if (append.startswith("-")
        #             or append.startswith("+")) and append.endswith(';'):
        #         m = filterMethodDecl(append.strip(" "))
        #         if not m is None:
        #             inter.methods.append(m)
        #         append = ''

    return interfaces