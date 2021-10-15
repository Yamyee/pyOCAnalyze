import os

class Decl():
    name = ''
    superclass = ''
    propertys = []
    methods = []
    file = ''
    startline = 0
    endline = 0
    def __init__(self,name='',superclass='',propertys=[],methods=[]):
        self.name = name
        self.superclass = superclass
        self.propertys = propertys
        self.methods = methods
    
class Method(Decl):
    argments = []
    returnType = ''
    isStatic = False
    required = True
    def __init__(self, name='',superclass='',propertys=[],methods=[],isStatic=False,argments=[],returnType='',required=True):
        super(Method, self).__init__(name=name,superclass=superclass,propertys=propertys,methods=methods)
        self.isStatic = isStatic
        self.argments = argments
        self.returnType = returnType
        self.required = required

class Interface(Decl):
    def __init__(self, name='',superclass='',propertys=[],methods=[]):
        super(Interface, self).__init__(name=name,superclass=superclass,propertys=propertys,methods=methods)

class Implementation(Decl):
    def __init__(self, name='',superclass='',propertys=[],methods=[]):
        super(Implementation, self).__init__(name=name,superclass=superclass,propertys=propertys,methods=methods)

class Property(Decl):
    type = ''
    var = ''
    modifiers = []
    isStatic = False
    def __init__(self,  name='',superclass='',propertys=[],methods=[],type='',modifiers=[],isStatic=False,var=''):
        super(Property, self).__init__(name=name,superclass=superclass,propertys=propertys,methods=methods)
        self.type = type
        self.modifiers = modifiers
        self.isStatic = isStatic
        self.var = var
        
class Protocol(Decl):
    def __init__(self, name='',superclass='',propertys=[],methods=[]):
        super(Protocol, self).__init__(name=name,superclass=superclass,propertys=propertys,methods=methods)
        
class File():
    interfaces = []
    methods = []
    protocols = []