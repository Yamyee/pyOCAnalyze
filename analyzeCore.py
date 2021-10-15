import os,sys
import baseClass
from analyzeInterface import interfaceAnalyze
files = []

def runPaths(path):
    for parent,dirList,fileList in os.walk(path):
        for fileName in fileList:
            if fileName.endswith(".h") or fileName.endswith(".m"):
                readFile(os.path.join(parent,fileName))
        for dirName in dirList:
            #递归
            runPaths(os.path.join(parent,dirName))

def readFile(path):
    contents = []
    print('analyzing... '+path)
    with open(path,'r+') as f:
        for line in f.readlines():
            if line.startswith("#") or line.startswith("//"):
                continue
            if line == '\n' or line == ' ' or line == '\t':
                continue
            l = line.lstrip('\t').lstrip(' ').rstrip('\t').rstrip('\n').rstrip(' ')
            contents.append(l)

    if len(contents) == 0:
        print('文件为空：{}'.format(path))
        return
    
    f = baseClass.File()
    if path.endswith('.h'):
        inters = interfaceAnalyze(contents)
        for i in inters:
            f.interfaces.append(i)
    
    for inter in f.interfaces:
        for pro in inter.propertys:
            print(pro.modifiers)
if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) == 0:
        print('请输入文件/文件夹路径')
    else:
        if os.path.isdir(argv[0]):
            runPaths(argv[0])
        else:
            readFile(argv[0])