from analyzeCore import analyze,protocols,interfaces,classes,implementations
import sys

ignoreClass = []
checkClass = ['Diff','Core']

lostMethods = []

def checkClassEnable(name):
    if len(checkClass) == 0:
        return True
    
    for c in checkClass:
        if c in name:
            return True

    return False

def needIgnore(name):
    if len(ignoreClass) == 0:
        return False

    for i in ignoreClass:
        if i in name:
            return True

    return False

def protocolMethodInClass(protocol,cls):
    allClsMethods = cls.methods.keys()
    allProMethods = protocol.methods.keys()
    if len(allClsMethods) == 0 or len(allProMethods) == 0:
        return 
    for met in allProMethods:
        if met in allClsMethods:
            continue
        sym = "+" if met.isStatic else "-"
        lm = "{} : {}[{} {}]".format(protocol.name,sym,cla.name,met.name)
        lostMethods.append(lm)

def diffCheck():
    print('比较差异化...')
    protocolKeys = protocols.keys()
    for cla in classes.values():
        # 忽略
        if needIgnore(cla.name) or not checkClassEnable(cla.name):
            continue
        print(cla.name+"...")
        for p in cla.protocols:
            # 忽略
            if needIgnore(p) or not checkClassEnable(p):
                continue
            if p not in protocolKeys:
                continue
            protocolMethodInClass(p,cla)


def output(path):

    if len(lostMethods) == 0:
        return
    content = "\n".join(lostMethods)
    with open(path,'w+') as f:
        f.write(content)

def collectMethods(path):
    print('收集方法...')
    content = "================\n"
    for cla in classes.values():
        
        for method in cla.methods:
            sym = "+" if method.isStatic else "-"
            mth = "{}[{} {}]".format(sym,cla.name,method.name)
            print(mth)
            content += mth + "\n"
        content += "================\n"

    if len(content) == 0:
        return
    with open(path,'w+') as f:
        f.write(content)
def main():

    if len(sys.argv) == 1:
        print('python3 checkDiffProtocol.py 扫描的文件/文件夹路径 输出结果文件路径')
        return
    path = sys.argv[1]
    if "," in path:
        for p in path.split(','):
            if len(p) > 0:
                analyze(p)
    else:
        analyze(path)
    collectMethods(sys.argv[2])
    # diffCheck()
    # output(sys.argv[2])

if __name__ == '__main__':
    main()
    