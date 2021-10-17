import baseClass
import parse
from analyzeInterface import filterMethodDecl

define = '@implementation'
end = '@end'
static = '@static'
synthesize = '@synthesize'


def parseImpName(line):
    if "(" in line:
        return parse.filterContent(line, define, "(")
    return line.replace(define, "").replace(" ", "")


def parseImplementation(contents):
    has = False
    imps = []
    im = baseClass.Implementation()
    append = ''

    for line in contents:
        if line.startswith(define):
            has = True
            im.name = parseImpName(line)
        elif has and line.startswith(end):
            imps.append(im)
            im = baseClass.Implementation()
            has = False
        elif has:
            if line.startswith('+') or line.startswith('-'):
                append = ''
            append += line
            if not append.endswith('{'):
                append += " "
            if (append.startswith("-")
                    or append.startswith("+")) and append.endswith('{'):
                m = filterMethodDecl(append.strip(" "), "{")
                if not m is None:
                    im.methods.append(m)
                append = ''

    return imps