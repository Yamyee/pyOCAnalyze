import os

class Decl():
    name = ''
    superclass = ''
    propertys = []
    methods = []
    file = ''
    startline = 0
    endline = 0
    def __init__(self,name,superclass='',propertys=[],methods=[]):
        self.name = name
        self.superclass = superclass
        self.propertys = propertys
        self.methods = methods
    
class Method(Decl):
    argments = []
    returnType = ''
    isStatic = False
    required = True
    def __init__(self, *args,isStatic=False,argments=[],returnType='',required=True):
        super(Method, self).__init__(*args)
        self.isStatic = isStatic
        self.argments = argments
        self.returnType = returnType
        self.required = required

class Property(Decl):
    type = ''
    modifiers = []
    isStatic = False
    def __init__(self, *args,type='',modifiers=[],isStatic=False):
        super(Property, self).__init__(*args)
        self.type = type
        self.modifiers = modifiers
        self.isStatic = isStatic

class Protocol(Decl):
    def __init__(self, *args):
        super(Protocol, self).__init__(*args)
        