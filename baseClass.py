import os

class Decl():
    def __init__(self, name=''):
        self.name = name
    def desc(self):
        return ""

#全局变量
class Define(Decl):
    def __init__(self, name='', value=''):
        super(Define, self).__init__(name=name)
        self.value = value
class Param(Decl):
    def __init__(self, name='', type=''):
        super(Param, self).__init__(name=name)
        self.type = type

    def desc(self):
        return "type = {},name = {}".format(self.type, self.name)

class Method(Decl):
    def __init__(self,
                 name='',
                 isStatic=False,
                 params=[],
                 returnType='',
                 required=True):
        super(Method, self).__init__(name=name)
        self.isStatic = isStatic
        self.params = params
        self.returnType = returnType
        self.required = required

    def desc(self):
        t = "+" if self.isStatic else "-"
        return "{}[{}]".format(t, self.name)


class Interface(Decl):
    def __init__(self,
                 name='',
                 superclass='',
                 propertys=[],
                 methods=[],
                 protocols=[]):
        super(Interface, self).__init__(name=name)
        self.superclass = superclass
        self.propertys = propertys
        self.methods = methods
        self.protocols = protocols

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
    def __init__(self, name='', methods=[]):
        super(Implementation, self).__init__(name=name)
        self.methods = methods

    def desc(self):
        methodDesc = ""
        for m in self.methods:
            methodDesc += m.desc()
            methodDesc += "\n"
        return "name = {}\nmethods = \n{}".format(self.name, methodDesc)


class Property(Decl):
    def __init__(self,
                 name='',
                 type='',
                 modifiers=[],
                 isStatic=False,
                 required=True):
        super(Property, self).__init__(name=name)
        self.type = type
        self.modifiers = modifiers
        self.isStatic = isStatic
        self.required = required

    def desc(self):
        return "type = {}\nname = {}\nmodifiers = {}\nisStatic = {}".format(
            self.type, self.name, str(self.modifiers), self.isStatic)


class Protocol(Decl):
    def __init__(self, name='', propertys=[], methods=[], superprotocols=[]):
        super(Protocol, self).__init__(name=name)
        self.superprotocols = superprotocols
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


class OCClass(Decl):
    def __init__(self, name='', protocols=[], propertys=[], methods=[]):
        super(OCClass, self).__init__(name=name)
        self.protocols = protocols
        self.propertys = propertys
        self.methods = methods
class File():
    def __init__(self,
                 interfaces=[],
                 implementations=[],
                 protocols=[],
                 defines=[],
                 imports=[],
                 total={}):
        self.interfaces = interfaces
        self.implementations = implementations
        self.protocols = protocols
        self.defines = defines
        self.imports = imports
        self.total = total

    def mapping(self):
        for i in self.interfaces + self.protocols + self.implementations + self.defines:
            self.total[i.name] = i