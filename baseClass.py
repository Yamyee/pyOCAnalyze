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


class Param(Decl):
    type = ""

    def __init__(self, name='', type=''):
        super(Param, self).__init__(name=name)
        self.type = type

    def desc(self):
        return "type = {},name = {}".format(self.type, self.name)


class Method(Decl):
    params = []
    returnType = ''
    isStatic = False
    required = True

    def __init__(self,
                 name='',
                 propertys=[],
                 methods=[],
                 isStatic=False,
                 params=[],
                 returnType='',
                 required=True):
        super(Method, self).__init__(name=name,
                                     propertys=propertys,
                                     methods=methods)
        self.isStatic = isStatic
        self.params = params
        self.returnType = returnType
        self.required = required

    def desc(self):
        t = "+" if self.isStatic else "-"
        return "{}[{}]".format(t, self.name)


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
        proDesc = "["
        for p in self.propertys:
            proDesc += p.desc()
            proDesc += "\n"
        proDesc += "]\n"
        methodDesc = ""
        for m in self.methods:
            methodDesc += m.desc()
            methodDesc += "\n"

        return "name = {}\nsuperclass = {}\nprotocols= {} \npropertys = \n{}methods = \n{}".format(
            self.name, self.superclass, str(self.protocols), proDesc,
            methodDesc)


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
        proDesc = "["
        for p in self.propertys:
            proDesc += p.desc()
            proDesc += "\n"
        proDesc += "]\n"
        methodDesc = ""
        for m in self.methods:
            methodDesc += m.desc()
            methodDesc += "\n"

        return "name = {}\nsuperprotocols = {}\npropertys = \n{}methods = \n{}".format(
            self.name, self.superprotocols, proDesc, methodDesc)


class File():
    interfaces = []
    implementations = []
    protocols = []
    defines = []
    #用类名，协议名，变量映射对应的类，协议，变量，方便查找
    total = {}

    def mapping(self):
        for i in self.interfaces + self.protocols + self.implementations + self.defines:
            self.total[i.name] = i