import baseClass
import parse
from analyzeInterface import filterProperty

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
    proto = baseClass.Protocol()
    for line in content:
        #@interface开头
        if line.startswith(define):
            proto.name = filterProtocolName(line)
            proto.superprotocols = filterSuperProtcols(line)
            has = True
        #@end 结束
        if has and line.startswith(end):
            protocols.append(proto)
            proto = baseClass.Protocol()
            has = False

        if has and line.startswith(prop):
            p = filterProperty(line)
            if not p is None:
                proto.propertys.append(p)

    return protocols