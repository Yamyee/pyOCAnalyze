import os

class Decl():
    def __init__(self):
        self.name = ''
    def desc(self):
        return ""

#全局变量
class Define(Decl):
    def __init__(self):
        super(Define, self).__init__()
        self.name = ''
        self.type = ''
class Param(Decl):
    def __init__(self):
        super(Param, self).__init__()
        self.name = ''
        self.type = ''

    def desc(self):
        return "type = {},name = {}".format(self.type, self.name)

class Method(Decl):
    def __init__(self):
        super(Method, self).__init__()
        self.name = ''
        self.isStatic = False
        self.params = []
        self.returnType = ''
        self.required = True

    def desc(self):
        t = "+" if self.isStatic else "-"
        return "{}[{}]".format(t, self.name)


class Interface(Decl):
    def __init__(self):
        super(Interface, self).__init__()
        self.name = ''
        self.superclass = ''
        self.propertys = []
        self.methods = []
        self.protocols = []

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
    def __init__(self):
        super(Implementation, self).__init__()
        self.name = ''
        self.methods = []

    def desc(self):
        methodDesc = ""
        for m in self.methods:
            methodDesc += m.desc()
            methodDesc += "\n"
        return "name = {}\nmethods = \n{}".format(self.name, methodDesc)


class Property(Decl):
    def __init__(self):
        super(Property, self).__init__()
        self.name = ''
        self.type = ''
        self.modifiers = []
        self.isStatic = False
        self.required = True

    def desc(self):
        return "type = {}\nname = {}\nmodifiers = {}\nisStatic = {}".format(
            self.type, self.name, str(self.modifiers), self.isStatic)


class Protocol(Decl):
    def __init__(self):
        super(Protocol, self).__init__()
        self.name = ''
        self.superprotocols = []
        self.propertys = []
        self.methods = []

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
    def __init__(self):
        super(OCClass, self).__init__()
        self.protocols = []
        self.propertys = []
        self.methods = []
class File():
    def __init__(self):
        self.path = ''
        self.interfaces = []
        self.implementations = []
        self.protocols = []
        self.defines = []
        self.imports = []
        self.total = {}

    def mapping(self):
        for i in self.interfaces + self.protocols + self.implementations + self.defines:
            self.total[i.name] = i