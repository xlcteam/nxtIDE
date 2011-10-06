#!/usr/bin/env python
import ast_template
import sys
from definitions import *
from compiler.consts import *
import os


class SecondPassVisitor(ast_template.Visitor):
    """This object goes through and output the code"""

    def __init__(self, fv, stream=sys.stdout, debug=False, root="./"):

        ast_template.Visitor.__init__(self,stream,debug)
    
        
        self.fv=fv  # first-pass visitor
        self.stream=stream
        self.erase_assign=False
        self.buffer=[]
        self.semicolon=True

        self.writef('#include "NXCDefs.h"\n')
        self.writef(open(os.path.join(root,"MyDefs.h"),'rt').read())
            
        
        for d in fv.defines:
            self.writef('#define %s %s\n' % (d[0],d[1]))
        
        self.print_structure_definitions(fv.struct_types)
        
        self.print_typedefs(fv.typedefs)

        if self.debug:
            print "Module Variables Printing "
        
        # print "module fn:", fv.functions['module'].variables
        self.print_variable_definitions(fv.functions['module'].variables)
        self.scope=['module']
        
        
    def type2str(self,datatype):
        if datatype=='Integer':
            return 'int'
        elif datatype=='IntegerPtr':
            return 'int&'
        elif datatype=='Word':
            return 'word'
        elif datatype=='Long':
            return 'long'
        elif datatype=='Byte':
            return 'byte'
        elif datatype=='Short':
            return 'short'
        elif datatype=='String':
            return 'string'
        elif datatype=='Mutex':
            return 'mutex'
        elif datatype in self.fv.struct_types:
            return datatype
        else:
            return 'int'

    def print_typedefs(self,typedefs):
        
        for types in typedefs:
            self.write('typedef %s %s;' % (typedefs[types],types))
            self.NEWLINE()
            self.flush()
            
    def print_structure_definitions(self,struct_types):
        
        for key in struct_types:
            self.write('struct %s ' % key)
            self.INDENT()
            variables=struct_types[key]
            for var in variables:
                self.write(self.type2str(variables[var].datatype))
                self.write(' %s' % variables[var].name)
                self.write(';')
                self.NEWLINE()
            self.DEDENT()
            self.write(';')
            self.NEWLINE()
        
        
    def print_variable_definitions(self,variables):
        for var in variables:
            
            
            if self.debug:
                print "  Variable ",variables[var]
            
            self.write(self.type2str(variables[var].datatype))

            self.write(' %s' % variables[var].name)
                
            if not variables[var].value is None:
                if isinstance(variables[var].value,list):
                    self.write('[]')
                    if not variables[var].value==[]:
                        self.write('={')
                        for v in variables[var].value:
                            self.write(v.__repr__())
                            if not v == variables[var].value[-1]:
                                self.write(',')
                        self.write('}')
                                
                            
                        
                else:
                    val=variables[var].value.__repr__()
                    self.write('= %s' % val.replace("'",'"'))
            self.write(';')
            self.NEWLINE()
            
            if variables[var].datatype in self.fv.struct_types:
                variables2=self.fv.struct_types[variables[var].datatype]
                for var2 in variables2:
                    if variables2[var2].value:
                        val2=variables2[var2].value.__repr__()
                        
                        self.write('%s.%s' % (var,variables2[var2].name))
                        self.write('= %s' % val2.replace("'",'"'))
                        self.write(';')
                        self.NEWLINE()
                
            
            
        self.flush()
        
        
    def flush(self):
        
        if self.buffer:
            for s in self.buffer:
                s=s.replace("'",'"')
                self.stream.write(s)
        
        self.buffer=[]
            
    def DEDENT(self,with_semicolon=False):
        self.indents -=1
        self.NEWLINE()
        self.write('}')
        if with_semicolon:
            self.write(';')
        self.NEWLINE()

    def INDENT(self):
        self.indents += 1
        self.write(' {')
        self.NEWLINE()

    def NEWLINE(self):
        self.write('\n')
        self.write(' ' * 4 * self.indents )
        
    def write(self, data):
        self.buffer.append(data)
            

    def writef(self, data):
        self.write(data)
        self.flush()

        
    def visitBlock(self, block):
        self.INDENT()
        self.v(block)
        self.DEDENT()

    def visitAdd(self, node):
        self.write("(")
        self.v(node.left)
        self.write(" + ")
        self.v(node.right)
        self.write(")")

    def visitAnd(self, node):
        self.write("(")
        for i in range(len(node.nodes)):
            self.write("(")
            self.v(node.nodes[i])
            self.write(")")
            if i < (len(node.nodes) - 1):
                self.write(" && ")
        self.write(")")

    def visitAssAttr(self, node):
        if self.debug:
            print 'visitSecondVisitorAssAttr'
        self.v(node.expr, self)
        self.write(".%s" % node.attrname)

    def visitAssName(self, node):
        self.write(node.name)

    def visitAssign(self, node):
        self.flush()
        self.erase_assign=False
        n=node.nodes[0]


        if self.scope[-1]=='module':
            return

#        try:
#            if (n.name == n.name.upper()) and (len(n.name)>2):  # a definition
#                return
#        except AttributeError:
#            pass   # probably a subscript?
            
        for i in range(len(node.nodes)):
            n = node.nodes[i]
            self.v(n)
            if i < len(node.nodes):
                self.write(" = ")
        self.v(node.expr)
        
        self.write("; ")
        self.NEWLINE()

        
        if self.erase_assign:
            self.buffer=[]

        self.flush()
        
        
    def visitAugAssign(self, node):
        self.v(node.node)
        self.write(" %s " % node.op)
        self.v(node.expr)
        self.write("; ")
        self.NEWLINE()


    def visitBitand(self, node):
        for i in range(len(node.nodes)):
            self.v(node.nodes[i])
            if i < (len(node.nodes) - 1):
                self.write(" & ")

    def visitBitor(self, node):
        for i in range(len(node.nodes)):
            self.v(node.nodes[i])
            if i < (len(node.nodes) - 1):
                self.write(" | ")

    def visitBitxor(self, node):
        for i in range(len(node.nodes)):
            self.v(node.nodes[i])
            if i < (len(node.nodes) - 1):
                self.write(" ^ ")        

    def visitBreak(self, node):
        self.write("break; ")
        self.NEWLINE()
        
    def visitFunction(self, node):
        self.scope.append('function')
    
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

        if ndefaults:
            for i in range(ndefaults):
                defargs.append((newargs.pop(), node.defaults.pop()))
            defargs.reverse()

        func_type=self.fv.functions[node.name].datatype
        if not func_type:
            func_type='void'
            
        if func_type=='default':
            func_type='int'
            
        if node.name=='main':
            self.write("task %s(" % node.name)
        elif node.name.find('task_')==0:
            self.write("task %s(" % node.name)
        elif node.name.find('sub_')==0:
            self.write("sub %s(" % node.name)
        elif node.name.find('inline_')==0:
            self.write("inline %s %s(" % (func_type,node.name.replace('inline_','')))
        else: 
            self.write("%s %s(" % (func_type,node.name))
        

        for i in range(len(newargs)):
            if isinstance(newargs[i], tuple):
                self.write("(%s, %s)" % newargs[i])
            else:
                self.write("int "+newargs[i])
            if i < len(newargs) - 1:
                self.write(", ")
        if defargs and len(newargs):
            self.write(", ")

        for i in range(len(defargs)):
            name, default = defargs[i]
            typename=default.node.name
            
            
            
            self.write("%s %s" % (self.type2str(typename),name))
            #self.v(default)
            if i < len(defargs) - 1:
                self.write(", ")
        
        if vararg:
            if (newargs or defargs):
                self.write(", ")
            self.write(vararg)
        if kwarg:
            if (newargs or defargs or vararg):
                self.write(", ")
            self.write(kwarg)

        self.write(") ")
        self.INDENT()
        
        self.print_variable_definitions(self.fv.functions[node.name].variables)
        
        self.v(node.code)
        self.DEDENT()
        
        self.flush()
        self.scope.pop()
            
        
    def visitCallFunc(self, node):
        
        name=node.node.name
        
        if name=="ASM":  # raw ASM
            s=node.args[0].value
            
            self.write("asm{%s}" % s)
            
            return
        
        if name=="NXC":
            s=node.args[0].value
            
            self.write("%s" % s)
            
            return
        
        if name=="DEFINE":
            s=node.args[1].value
            d=node.args[0].value

            self.write("#define %s %s" %(d,s))
            self.NEWLINE()
            self.semicolon=False
            return
        
        self.v(node.node)
        self.write("(")
        for i in range(len(node.args)):
            self.v(node.args[i])
            if i < (len(node.args) - 1):
                self.write(", ")
        if node.star_args:
            if len(node.args):
                self.write(", ")
            self.write("*")
            self.v(node.star_args)
        if node.dstar_args:
            if node.args or node.star_args:
                self.write(", ")
            self.write("**")
            self.v(node.dstar_args)
        self.write(")")

        if name in self.fv.types:
            self.erase_assign=True
        
        
    def visitClass(self, node):
        self.scope.append('class')

        self.flush()
        for i in range(len(node.bases)):
            self.v(node.bases[i])
        self.INDENT()
        self.v(node.code)
        self.DEDENT()
        
        self.buffer=[]  # get rid of all of the stuff in a class def
        self.scope.pop()
        
        
    def visitCompare(self, node):
        self.write("(")
        self.v(node.expr)
        
        for operator, operand in node.ops:
            self.write(" %s " % operator)
            self.v(operand)
        self.write(")")

    def visitConst(self, node):
        self.write(repr(node.value))

    def visitContinue(self, node):
        self.write("continue; ")

    def visitDiscard(self, node):
        self.semicolon=True

        # deal with empty statements, so it doesn't print None
        try:
            if node.expr.value is None:
                pass
            else:
                self.v(node.expr)
                if self.semicolon:
                    self.write(";")
                self.NEWLINE()
        except AttributeError:
            self.v(node.expr)
            if self.semicolon:
                self.write(";")
            self.NEWLINE()

    def visitDiv(self, node):
        self.v(node.left)
        self.write(" / ")
        self.v(node.right)


    def visitFor(self, node):
        
        
        children=node.list.getChildNodes()
        start='0'
        end='1'
        step='1'
        
        if self.debug:
            print node.assign.name
            print dir(node.assign)
            
            print node.list
            print dir(node.list)
    
            print node.list.getChildren()

            print children
            
        if children[0].name=='range':
            vals=[v.asList()[0] for v in children[1:]]
            print "vals:", vals
            if node.assign.name=='repeat':  # keyword repeat
                if len(vals)==1:
                    end=vals[0]
                else:
                    raise ValueError,"Bad for-loop construction"
                
                self.write("repeat(%s) " % (end))
                
            else:
                if len(vals)==1:
                    end=vals[0]
                elif len(vals)==2:
                    start=vals[0]
                    end=vals[1]
                elif len(vals)==3:
                    start=vals[0]
                    end=vals[1]
                    step=vals[2]
                else:
                    raise ValueError,"Bad for-loop construction"
                
                varname=node.assign.name
                self.write("for (%s=%s; %s<%s; %s+=%s) " % (varname,start,
                                                            varname,end,
                                                            varname,step))

            self.INDENT()
            self.v(node.body)
            self.DEDENT()
        else:
            raise ValueError,"For-loop construction not implemented"
            
        
        
        
    def visitGenExpr(self, node):
        self.write("(")
        self.v(node.code)
        self.write(")")

    def visitGetattr(self, node):
        self.v(node.expr)
        self.write(".%s" % node.attrname)

    def visitIf(self, node):
        flag=False
        for c, b in node.tests:
            if not flag:
                self.write("if (")
            else:
                self.write("else if (")
            self.v(c)
            self.write(') ')
            self.INDENT()
            self.v(b)
            self.DEDENT()
            flag=True
        if node.else_:
            self.write("else ")
            self.INDENT()
            self.v(node.else_)
            self.DEDENT()
            
    def visitKeyword(self, node):
        self.write(node.name)
        self.write("=")
        self.v(node.expr)


    def visitInvert(self, node):
        self.write("~")
        self.v(node.expr)

    def visitLeftShift(self, node):
        self.v(node.left)
        self.write(" << ")
        self.v(node.right)

    def visitMod(self, node):
        self.v(node.left)
        self.write(" % ")
        self.v(node.right)

    def visitMul(self, node):
        self.v(node.left)
        self.write(" * ")
        self.v(node.right)

    def visitName(self, node):
        
        if node.name=='False':
            self.write("false")
        elif node.name=='True':
            self.write("true")
        else:
            self.write(node.name.replace('inline_',''))

    def visitNot(self, node):
        self.write(" !(")
        self.v(node.expr)
        self.write(")")
        
    def visitOr(self, node):
        self.write("(")
        for i in range(len(node.nodes)):
            self.write("(")
            self.v(node.nodes[i])
            self.write(")")
            if i < len(node.nodes) - 1:
                self.write(" || ")
        self.write(")")

                
    def visitPass(self, node):
        self.write("// pass ")

    def visitReturn(self, node):
        try:
            if node.value.value is None:
                self.write('return;')
            else:
                self.write('return(%s);' % node.value.value.__repr__())
                
        except TypeError:
            pass
        except AttributeError:
                
            self.write("return(")
            self.v(node.value)
            self.write(");")

    def visitRightShift(self, node):
        self.v(node.left)
        self.write(" >> ")
        self.v(node.right)

    def visitSubscript(self, node):
        isdel = False
        if node.flags == OP_DELETE: isdel = True
        isdel and self.write("del ")
        self.v(node.expr)
        self.write("[")
        for i in range(len(node.subs)):
            self.v(node.subs[i])
            if i == len(node.subs) - 1:
                self.write("]")
        node.flags == OP_DELETE and self.NEWLINE()

    def visitSub(self, node):
        self.write("(")
        self.v(node.left)
        self.write(" - ")
        self.v(node.right)
        self.write(")")

    def visitUnaryAdd(self, node):
        self.write("+")
        self.v(node.expr)

    def visitUnarySub(self, node):
        self.write("-")
        self.v(node.expr)

    def visitWhile(self, node):
        self.write("while (")
        self.v(node.test)
        self.write(") ")
        self.INDENT()
        self.v(node.body)
        if node.else_:
            self.DEDENT()
            self.write("else:")
            self.INDENT()
            self.v(node.else_)
        self.DEDENT()
        
     

