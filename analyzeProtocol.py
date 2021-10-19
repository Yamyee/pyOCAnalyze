import baseClass
import parse
from analyzeInterface import filterProperty
from analyzeInterface import filterMethodDecl

define = '@protocol'
end = '@end'
prop = '@property'


def filterProtocolName(line):
    if not line.startswith(define):
        return ''
    return parse.filterContent(line, define, "<")


def filterSuperProtcols(line):
    if "<" not in line or ">" not in line:
        return []
    return parse.filterArr(line, "<", ">", ",")


def parseProtocol(content):
    has = False
    protocols = []
    append = ''
    for line in content:
        #@interface开头
        if line.startswith(define):
            proto = baseClass.Protocol(name='',propertys=[],methods=[],superprotocols=[])
            proto.name = filterProtocolName(line)
            proto.superprotocols = filterSuperProtcols(line)
            has = True
        #@end 结束
        elif has and line.startswith(end):
            protocols.append(proto)
            has = False

        elif has and line.startswith(prop):
            p = filterProperty(line)
            if not p is None:
                proto.propertys.append(p)
        elif has:
            append += line
            if not append.endswith(';'):
                append += " "
            if (append.startswith("-")
                    or append.startswith("+")) and append.endswith(';'):
                m = filterMethodDecl(append.strip(" "))
                if not m is None:
                    proto.methods.append(m)
                append = ''
    return protocols