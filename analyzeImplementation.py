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
                append = ''
            append += line
            if not append.endswith('{'):
                append += " "
            if (append.startswith("-")
                    or append.startswith("+")) and append[-1] in methodEnds:
                m = filterMethodDecl(append.strip(" "), "{")
                if not m is None:
                    methods.append(m)
                append = ''

    return imps