#!/usr/bin/env python



class MyObject(object):
    
    def __init__(self,name,type='default'):
        
        self.name=name
        self.type=type
        self.datatype=None
        self.value=None


        self.variables=[]

    def __repr__(self):
        return "%s %s of datatype %s with value %s" % (self.type, self.name,
                self.datatype.__repr__(), self.value.__repr__())
        #return self.type+" "+self.name+" of datatype "+self.datatype.__repr__()+" with value "+self.value.__repr__()


class Variable(MyObject):
    
    def __init__(self,name,datatype='default'):
        
        
        super(Variable,self).__init__(name,'variable')
        self.datatype=datatype
    
        
class Function(MyObject):

    def __init__(self,name,variables=[]):
        
        
        super(Function,self).__init__(name,'function')
        self.variables=variables
        
 
