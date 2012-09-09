#!/usr/bin/env python
import ast_template
import sys
from definitions import *
from compiler.consts import *

        
class FirstPassVisitor(ast_template.Visitor):
    """This object goes through and gets all of the variables.  
    The second pass will output the code"""
    
    def __init__(self,stream=sys.stdout,debug=False):

        ast_template.Visitor.__init__(self,stream,debug)
        self.variables={}

        self.return_datatype=None
        self.types=['Byte','Short','Word','String','Mutex','Integer','Long','Struct']
        self.struct_types={}
        self.functions={}
        self.functions['module']=Function('module',self.variables)
        
        self.variables_assign=[]
        self.kwassign=[]
        self.use_kwassign=False
        
        self.typedefs={}
        
        self.scope=['module']
        
        self.use_typedef=False
        

    def visitClass(self, node):
        self.scope.append('class')
        
        variables={}
        old_self_variables=self.variables
        self.variables=variables
        
        if self.debug:
            print "myvisitClass"
            print node.name
        
        basename=node.bases[0].name
        for i in range(len(node.bases)):
            self.v(node.bases[i])
            
            
        self.use_typedef=False
        self.v(node.code)

        if self.use_typedef:
            self.typedefs[node.name]=basename
            self.types.append(node.name)
        else:
            self.struct_types[node.name]=variables
            self.types.append(node.name)
            self.variables=old_self_variables
        self.scope.pop()
        
        
        
    def visitPass(self, node):
        if self.scope[-1]=='class':
            self.use_typedef=True
        
    def visitBlock(self, block):
        if self.debug:
            print "myvisitBlock"
        self.v(block)

    def visitAssName(self, node):
        if self.debug:
            print 'visitAssName'
            if node.flags == OP_DELETE:
                print "del ",
            print node.name
        
        n=node
        
        self.variables_assign.append(n.name)
        

        if n.name not in self.variables:
            self.variables[n.name]=Variable(n.name)
            if self.debug:
                print "MyAddVar",n.name
        
    def visitReturn(self, node):
        #self.write("return ")
        #self.v(node.value)
        try:
            if node.value.value is None:
                self.return_datatype='void'
            else:
                if isinstance(node.value.value,int):
                    self.return_datatype='int'
                else:
                    raise TypeError,"Unknown type for "+str(node.value.value)
                
        except TypeError:
            pass
        except AttributeError:  # a name?
            name=node.value.name
            if name in self.variables:
                self.return_datatype=self.variables[name].datatype
            else:
                raise NameError, "Name"+name+"not found"
            
    def visitFor(self, node):
        if self.debug:
            print 'myvisitFor'

        if node.assign.name!='repeat':  # keyword repeat
            self.v(node.assign)
            
        self.v(node.body)
        
        
    
    def visitAssign(self, node):
        if self.debug:
            print 'MyvisitAssign'
            
        self.variables_assign=[]
        for i in range(len(node.nodes)):
            n = node.nodes[i]
            if self.debug:
                print "  Node ",n
            self.v(n)
            
        if self.debug:
            print "varassign ",self.variables_assign
            a=node.expr.asList()[0]
            print "varassign expr",node.expr,node.expr.asList()[0],type(a)
        
        if self.scope[-1]=='module':
            if self.debug:
                print "Module Variables"
            for name in self.variables_assign:
                val=node.expr.asList()[0]
                self.variables[name].value=val
                if isinstance(val,str):
                    self.variables[name].datatype='String'
                if self.debug:
                    print "  ",self.variables[name]
                
                
        self.v(node.expr)

        
    def visitKeyword(self, node):
        if self.debug:
            print 'myvisitKeyword'

        if not self.use_kwassign:
            self.v(node.expr)
            return
        
        
        
    def visitCallFunc(self, node):
        if self.debug:
            print 'myvisitCallFunc'
            print 'funcname: ',node.node.name
            
        name=node.node.name
        
        
        if not name in self.types:
            self.v(node.node)
            for i in range(len(node.args)):
                self.v(node.args[i])

            return
            
        for v in self.variables_assign:
            if (name=='Byte' or name=='Word' or name=='Short' or 
                name=='String' or name=='Integer' or name=='Long' or
                name=='Mutex'):
                    
                self.variables[v].datatype=name
                try:
                    self.variables[v].value=node.args[0].value
                except IndexError:
                    self.variables[v].value=None # to fix the mutex problem
                    # was:  pass  # use the default value
                except AttributeError:  # list? or mutex
                    nodelist=node.args[0].asList()
                    vallist=[]
                    for l in nodelist:
                        vallist.append(l.value)
                    
                    self.variables[v].value=vallist
            elif name=='Struct':
                    
                
                self.use_kwassign=True

                
                struct_name=node.args[0].value
                
                if not struct_name in self.struct_types:
                    self.struct_types.append(struct_name)
                    
                    for i in range(1,len(node.args)):
                        if self.debug:
                            print node.args[i]
                            print dir(node.args[i])
                        fun=node.args[i].name
                        #self.v(node.args[i])
                        if self.debug:
                            print "  fun",fun
            elif name in self.types:
                self.variables[v].datatype=name
                try:
                    self.variables[v].value=node.args[0].value
                except IndexError:
                    pass  # use the default value
                except AttributeError:  # list?
                    self.variables[v].value=[]
                
            
    def visitFunction(self, node):
        self.scope.append('function')
        self.return_datatype=None
        
        variables={}
        old_self_variables=self.variables
        self.variables=variables
        
        if self.debug:
            print "myvisitFunction"
            print node.name
        hasvar = haskw = hasone = hasboth = False

        ndefaults = len(node.defaults)

        if node.flags & CO_VARARGS:
            hasone = hasvar = True
        if node.flags & CO_VARKEYWORDS:
            hasone = haskw = True
        hasboth = hasvar and haskw

        kwarg = None
        vararg = None
        defargs = []
        newargs = node.argnames[:]


        self.v(node.code)
                
        self.functions[node.name]=Function(node.name,variables)
        self.functions[node.name].datatype=self.return_datatype
        self.variables=old_self_variables
        self.scope.pop()
                    
        
        # remove those variables that are global
        remove_var=[]
        for var in self.functions[node.name].variables:
            if (var in self.variables and 
                self.functions[node.name].variables[var].datatype=='default'):
                
                remove_var.append(var)
                    
        for r in remove_var:
            self.functions[node.name].variables.pop(r)
     
