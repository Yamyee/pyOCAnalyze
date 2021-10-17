import os, sys
import baseClass
from analyzeInterface import parseInterface
from analyzeProtocol import parseProtocol
from analyzeImplementation import parseImplementation
# files = []
protocols = {}
interfaces = {}
implementations = {}
classes = {}


def runPaths(path):
    for parent, dirList, fileList in os.walk(path):
        for fileName in fileList:
            if fileName.endswith(".h") or fileName.endswith(".m"):
                readFile(os.path.join(parent, fileName))
        for dirName in dirList:
            #递归
            runPaths(os.path.join(parent, dirName))


def readFile(path):
    contents = []
    print('analyzing... ' + path)
    with open(path, 'r+') as f:
        for line in f.readlines():
            if line.startswith("#") or line.startswith("//"):
                continue
            if line == '\n' or line == ' ' or line == '\t':
                continue
            l = line.lstrip('\t').lstrip(' ').rstrip('\t').rstrip('\n').rstrip(
                ' ')
            contents.append(l)

    if len(contents) == 0:
        print('文件为空：{}'.format(path))
        return

    inters = parseInterface(contents)

    for i in inters:
        interfaces[i.name] = i
        if i.name in implementations.keys():
            cl = baseClass.OCClass()
            for p in i.propertys:
                cl.propertys.append(p)
            for m in implementations[i.name].methods:
                cl.methods.append(m)
            classes[i.name] = cl

    protocols = parseProtocol(contents)

    for p in protocols:
        protocols[p.name] = p

    if path.endswith('.m'):

        imps = parseImplementation(contents)
        for i in imps:
            implementations[i.name] = i
            if i.name in interfaces.keys():
                cl = baseClass.OCClass()
                for p in interfaces[i.name].propertys:
                    cl.propertys.append(p)
                for m in i.methods:
                    cl.methods.append(m)
                classes[i.name] = cl


def compareClass():
    if len(classes) == 0 or len(protocols) == 0:
        return

    for cla in classes:

        for i in cla.interfaces:
            ms = []
            for p in i.protocols:
                if p.name not in protocols.keys():
                    print('protocol {} not found'.format(p.name))
                    continue
                else:
                    ms = p.methods

            if len(ms) == 0:
                continue

            for m in ms:
                if m not in cla.methods:
                    print('class {} undefind')


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) == 0:
        print('请输入文件/文件夹路径')
    else:
        if os.path.isdir(argv[0]):
            runPaths(argv[0])
        else:
            readFile(argv[0])

    # compareClass()