import re
import baseClass

define='@interface'
end='@end'
prop = '@property'
    
def interfaceAnalyze(content):
    has = False
    interfaces = []
    inter = baseClass.Interface()
    for line in content:

        if line.startswith(define):
            inter.name=line.replace(define,'').split(':')[0].lstrip(' ').rstrip(' ')
            supercls = ''
            if ":" in line:
                supercls = line.split(':')[1]
                if "<" in supercls:
                    supercls = supercls.split('<')[0].strip(' ')
            inter.superclass = supercls
            has = True

        if has and line.startswith(end):
            interfaces.append(inter)
            inter = baseClass.Interface()
            has = False
        if line.startswith(prop):
            l = line.replace(prop,'').replace('(','').lstrip(' ')
            arr = l.split(')')
            modifiers = arr[0].split(',')
            _property = baseClass.Property()
            _property.modifiers = modifiers
            s = arr[1].replace(';')
            sp = ' '
            if '*' in s :
                sp = '*'
            _property.type = s.split(sp)[0].strip(' ')
            _property.var = s.split(sp)[1].strip(' ')
            inter.propertys.append(_property)
    
    return interfaces