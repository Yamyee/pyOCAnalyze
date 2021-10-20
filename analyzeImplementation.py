import baseClass
import parse
from analyzeInterface import filterMethodDecl,filterCategory,methodEnds

define = '@implementation'
end = '@end'
static = '@static'
synthesize = '@synthesize'



def parseImpName(line):
    if "(" in line:
        return parse.filterContent(line, define, "(")
    return line.replace(define, "").replace(" ", "")

def parseMethodEnd(line):
    has = False
    sub = line
    for end in methodEnds:
        if end in sub:
            has = True
            sub = line.split(end)[0]
    return has,sub

def parseImplementation(contents):
    has = False
    imps = []
    append = ''
    methods = []
    for line in contents:
        if line.startswith(define):
            name=parseImpName(line)
            cat = filterCategory(line)
            if len(cat)>0:
                name += "({})".format(cat)
            has = True
        elif has and line.startswith(end):
            im = baseClass.Implementation()
            im.name = name
            im.methods = methods
            imps.append(im)
            methods = []
            has = False
        elif has:
            if line.startswith('+') or line.startswith('-'):
                append = line
            elif (append.startswith('-') or append.startswith('+')) and len(line) > 0 :
                append += " "+line
                isEnd,subLine = parseMethodEnd(append)
                if isEnd:
                    met = filterMethodDecl(subLine.strip(" "))
                    if not met is None:
                        methods.append(met)
                    append = ''             
    return imps