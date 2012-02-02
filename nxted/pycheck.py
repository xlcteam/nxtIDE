#!/usr/bin/env python

import sys, re, os
import compiler.ast
from compiler.visitor import ASTVisitor
from compiler import parse, walk
from compiler.consts import *

class Visitor(ASTVisitor): 
    def __init__(self, stream=sys.stdout, parent=None, debug=False):
        
        self.parent = parent

        self.v = lambda tree, visitor=self: walk(tree, visitor)
        self.stream = stream
        self.strcode = ""
        self.debug = debug
        self.indents = 0

        self.ids = {}
        self.ids['global'] = ['abs', 'str', 'ord', 'True', 'False', 'robot', 
                                'pygame', 'list', 'range', 'RoboException', 
                                'None', 'int', 'float', 'zip']
        self.ids['__fn__'] = []
        self.ids[''] = []

        self.fn_types = {}
        self.fn_type_regex = re.compile(":param \((.*?)\)")

        self.var_types = {}
        self.var_types['global'] = {}

        self.fn = ""
        ASTVisitor.__init__(self)
    
    def addId(self, name):
        if self.fn == "":
            self.ids['global'].append(name)
        else:
            self.ids[self.fn].append(name)

    def addVarType(self, name, type):
        if self.fn == "":
            self.var_types['global'][name] = type
        else:
            if not self.var_types.has_key(self.fn):
                self.var_types[self.fn] = {}
            
            self.var_types[self.fn][name] = type

            

    def __str__(self):
        return self.strcode
    
    def DEDENT(self):
        self.indents -=1
        self.NEWLINE()
            
    def INDENT(self):
        self.indents += 1
        self.NEWLINE()

    def NEWLINE(self):
        self.write('\n')
        self.write(' ' * 4 * self.indents )

    def write(self, data):
        if self.stream:
            self.stream.write(data)
        self.strcode += data
        
    def visitAssName(self, node):
        self.addId(node.name)
        
    def visitAssign(self, node):
        for i in range(len(node.nodes)):
            n = node.nodes[i]
            self.v(n)
        
        if isinstance(node.expr, compiler.ast.Const) and \
            isinstance(node.nodes[0], compiler.ast.AssName):

            self.addVarType(node.nodes[0].name, type(node.expr.value))

        self.v(node.expr)

    def visitAugAssign(self, node):

        self.v(node.node)
        self.v(node.expr)

    def visitCallFunc(self, node):
        if not isinstance(node.node, compiler.ast.Getattr):
            if not (node.node.name in self.ids['global']):
                #print node.node.name
                pass

        self.v(node.node)        

        for i in range(len(node.args)):
            #print "\t", node.args[i]
            #help(node.args[i])

            if isinstance(node.args[i], compiler.ast.Name):
                self.visitName(node.args[i])

            if isinstance(node.args[i], compiler.ast.Const) and \
                not isinstance(node.node, compiler.ast.Getattr) and \
                self.fn_types.has_key(node.node.name):

                if self.fn_types[node.node.name] == []:
                    continue
 
                if not self.istype(self.fn_types[node.node.name][i],
                    node.args[i].value):

                    fn_type = self.fn_types[node.node.name][i]
                    fn_name = node.node.name
                    var_type = type(node.args[i].value)
                    var_value = node.args[i].value

                    raise ValueError("%s expects %s not %s" % 
                                    (fn_name, fn_type, var_type.__name__),
                                *self.parent.first_match(fn_name, i, var_value))
                   

            if isinstance(node.args[i], compiler.ast.Name) and \
                not isinstance(node.node, compiler.ast.Getattr) and \
                self.fn_types.has_key(node.node.name):

                if self.fn_types[node.node.name] == []:
                    continue
                if not self.var_types.has_key(self.fn):
                    continue
                if not self.var_types[self.fn].has_key(node.args[i].name):
                    continue

                if not self.istype(self.fn_types[node.node.name][i],
                    self.var_types[self.fn][node.args[i].name]):

                    fn_type = self.fn_types[node.node.name][i]
                    fn_name = node.node.name
                    var_type = self.var_types[self.fn][node.args[i].name]
                    var_name = node.args[i].name

                   # self.parent.first_match(fn_name, i, var_name)
                    
                    raise ValueError("%s expects %s not %s" % 
                                    (fn_name, fn_type, var_type.__name__),
                                *self.parent.first_match(fn_name, i, var_name))
            
            self.v(node.args[i])

            
    def visitCompare(self, node):

        self.v(node.expr)
        for operator, operand in node.ops:
            self.v(operand)

    def visitFunction(self, node):
        self.ids[node.name] = []
        
        self.fn = "__fn__"
        self.addId(node.name)

        if isinstance(node.doc, str):
            self.fn_types[node.name] = self.parseDoc(node.doc)
        
        self.fn = node.name
        for x in node.argnames[:]:
            self.addId(x)


        self.v(node.code)
        self.fn = ""

    def visitIf(self, node):
            
        (c, b) = node.tests[0]
        self.v(c)
        self.v(b)
    
        for c, b in node.tests[1:]:
            self.v(c)
            self.v(b)
        if node.else_:
            self.v(node.else_)

    def visitKeyword(self, node):
        self.v(node.expr)

    def visitModule(self, node):
        self.v(node.node)

    def visitName(self, node):

        defined = node.name in self.ids[self.fn] \
            or node.name in self.ids['__fn__'] \
            or node.name in self.ids['global']

        
        if not defined:
            raise NameError("Name '%s' is not defined" % (node.name),
                            self.parent.first_occur(node.name))


    def visitStmt(self, node):
        for n in node.nodes:
            self.v(n)

    def visitWhile(self, node):
        self.v(node.test)
        self.v(node.body)
        if node.else_:
            self.v(node.else_)

    def visitImport(self, node):
        for name in node.asList()[0]:
            self.addId(name[0])

    def parseDoc(self, s):
        return self.fn_type_regex.findall(s)

    def istype(self, t, val):
        r = {'int': int, 'str': str}
        return isinstance(val, r[t])
    


class PyCheck():
    def __init__(self):
        self.src = None 

        self.visitor = Visitor(parent = self)

    def check(self, filename = None, string = None):
        if string != None:
            self.src = string
        else:
            self.src = open(filename).read()
        
        self.visitor.v(parse(self.src))

        return True
    

    def first_occur(self, name):
        line = 1
        for x in self.src.split('\n'):
            if name in x:
                return line

            line += 1
        return line
    
    def first_match(self, fn_name, narg, val):
        regex = '.*?%s\(%s\s*(%s)\).*?' % \
                (fn_name, '.*?,'*narg, val)

        match = re.search(regex, self.src)
        
        line = self.src.count(os.linesep, 0, match.start()) + 1

        return [line, (match.start(1), match.end(1)) ]
            

__lfix__ = "#lfixed"

def loopFix(s, fn):
    fix = __lfix__
    i = re.sub("([\t ]*)while\s(.*):\n", "\\1while \\2:\n\\1    %s%s\n" % \
                (fn,fix), s)
    i = re.sub("([\t ]*)for\s(.*):\n", "\\1for \\2:\n\\1    %s%s\n" % \
                (fn, fix), i)
    return i

def realLine(s, l):
    s = s.split('\n')
    fixes = []
    for line in s:
        if __lfix__ in line:
            fixes.append(1)
        else:
            fixes.append(0)

    return l - sum(fixes[:l])
        

if __name__ == "__main__":
    check = PyCheck()
    check.check("../nxtemu/api.py")
    check.check("files/test1.py")
   #check.check("etest.py")
    #print vi.ids
    #string = loopFix(open("etest.py").read(), "tester()") 
    #print string
    print loopFix("""def main():
    while 1:
        TextOut(0, LCD_LINE1, "socialny defekt")
        Wait(2000)""", "t()")
    print loopFix(open("files/whiletester.py").read(), "tester()")
    #print realLine(string, 30)
