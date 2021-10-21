import os, sys, re
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

filter='\/\*([\w\W]*?)\*\/'#匹配/**/包含的内容
filter1='\/\/(.*)'#匹配//后面的内容
filter2=['','\n','\t',' ']
def readFile(path):
    contents = []
    if not os.path.exists(path):
        print(path+" not found")
        return
    print('analyzing... ' + path)
    with open(path, 'r+') as f:
        all = ''.join(f.readlines())
        arr = re.findall(filter,all)
        if len(arr) > 0:
            for a in arr:
                all = all.replace('/*{}*/'.format(a),' ')
        # 这里还要去掉/**/包裹的注释

        allLines = all.split('\n')
        for line in allLines:
            sub = line
            marr = re.findall(filter1,line)
            if len(marr) > 0:
                for a in marr:
                    sub = line.replace('//{}'.format(a),' ')
            if sub.startswith("#") or sub.startswith("//"):
                continue
            sub = sub.lstrip('\t').lstrip(' ').rstrip('\t').rstrip('\n').rstrip(
                ' ')
            if sub in filter2:
                continue
            contents.append(sub)

    if len(contents) == 0:
        print('文件为空：{}'.format(path))
        return
    print('parsing interface...')
    inters = parseInterface(contents)

    for i in inters:
        interfaces[i.name] = i
        if i.name in implementations.keys():
            cl = baseClass.OCClass()
            cl.name = i.name
            for p in i.propertys:
                cl.propertys.append(p)
            print('interface '+i.name)
            print("protpertys count = "+str(len(i.propertys)))
            print("methods count = "+str(len(implementations[i.name].methods)))
            for m in implementations[i.name].methods:
                cl.methods.append(m)
            classes[i.name] = cl
    print('parsing protocol...')
    pros = parseProtocol(contents)

    for p in pros:
        protocols[p.name] = p

    if path.endswith('.m'):
        print('parsing implementation...')
        imps = parseImplementation(contents)
        for i in imps:
            implementations[i.name] = i
            if i.name in interfaces.keys():
                cl = baseClass.OCClass()
                cl.name = i.name
                props = interfaces[i.name].propertys
                print('interface '+i.name)
                print("protpertys count = "+str(len(props)))
                print("methods count = "+str(len(i.methods)))
                for p in props:
                    cl.propertys.append(p)
                for m in i.methods:
                    cl.methods.append(m)
                classes[i.name] = cl
    print('end... ' + path)

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

def analyze(path):
    if os.path.isdir(path):
        runPaths(path)
    else:
        readFile(path)

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) == 0:
        print('请输入文件/文件夹路径')
    else:
        analyze(argv[0])

    # compareClass()