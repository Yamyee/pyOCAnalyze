import baseClass
import parse
from analyzeInterface import filterMethodDecl,filterCategory

define = '@implementation'
end = '@end'
static = '@static'
synthesize = '@synthesize'

methodEnds = [";","{","//"]

def parseImpName(line):
    if "(" in line:
        return parse.filterContent(line, define, "(")
    return line.replace(define, "").replace(" ", "")


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
                if line[0] in methodEnds:
                    met = filterMethodDecl(append.strip(" "), "{")
                    if not met is None:
                        methods.append(met)
                    append = ''             
                else:
                    append += line
    return imps