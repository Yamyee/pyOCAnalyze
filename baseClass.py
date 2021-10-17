import os


#全局变量
class Define():
    protectLevel = 'public'
    name = ""
    value = ""


class Decl():
    name = ''
    file = ''
    startline = 0
    endline = 0

    def __init__(self, name='', propertys=[], methods=[]):
        self.name = name
        self.propertys = propertys
        self.methods = methods

    def desc(self):
        return ""


class Method(Decl):
    argments = []
    returnType = ''
    isStatic = False
    required = True

    def __init__(self,
                 name='',
                 propertys=[],
                 methods=[],
                 isStatic=False,
                 argments=[],
                 returnType='',
                 required=True):
        super(Method, self).__init__(name=name,
                                     propertys=propertys,
                                     methods=methods)
        self.isStatic = isStatic
        self.argments = argments
        self.returnType = returnType
        self.required = required


class Interface(Decl):
    superclass = ""
    protocols = []
    propertys = []
    methods = []

    def __init__(self,
                 name='',
                 superclass='',
                 propertys=[],
                 methods=[],
                 protocols=[]):
        super(Interface, self).__init__(name=name)
        self.superclass = superclass
        self.protocols = protocols
        self.methods = methods

    def desc(self):
        proDesc = ""
        for p in self.propertys:
            proDesc += "[" + p.desc() + "]"
        return "name = {}\nsuperclass = {}\nprotocols= {} \npropertys = \n{}".format(
            self.name, self.superclass, str(self.protocols), proDesc)


class Implementation(Decl):
    def __init__(self, name='', propertys=[], methods=[]):
        super(Implementation, self).__init__(name=name,
                                             propertys=propertys,
                                             methods=methods)


class Property(Decl):
    type = ''
    name = ''
    modifiers = []
    isStatic = False
    required = True

    def __init__(self, type='', modifiers=[], isStatic=False, name=''):
        super(Property, self).__init__(name=name)
        self.type = type
        self.modifiers = modifiers
        self.isStatic = isStatic
        self.name = name

    def desc(self):
        return "type = {}\nname = {}\nmodifiers = {}\nisStatic = {}".format(
            self.type, self.name, str(self.modifiers), self.isStatic)


class Protocol(Decl):
    superprotocols = []
    propertys = []
    methods = []

    def __init__(self, name='', propertys=[], methods=[], superpros=[]):
        super(Protocol, self).__init__(name=name)
        self.superprotocols = superpros
        self.propertys = propertys
        self.methods = methods

    def desc(self):
        proDesc = ""
        for p in self.propertys:
            proDesc += "[" + p.desc() + "]"
        return "name = {}\nsuperprotocols = {}\npropertys=\n{}".format(
            self.name, self.superprotocols, proDesc)


class File():
    interfaces = []
    implementations = []
    protocols = []
    defines = []
    #用类名，协议名，变量映射对应的类，协议，变量，方便查找
    totoal = {}