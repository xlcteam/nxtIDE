#!/usr/bin/env python

import sys, re
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
        self.debug=debug
        self.indents = 0

        self.ids = {}
        self.ids['global'] = ['abs', 'str', 'ord', 'True', 'False', 'robot', 
                                'pygame', 'list', 'range', 'RoboException', 
                                'None']
        self.ids['__fn__'] = []
        self.ids[''] = []

        self.fn = ""
        ASTVisitor.__init__(self)
    
    def addId(self, name):
        if self.fn == "":
            self.ids['global'].append(name)
        else:
            self.ids[self.fn].append(name)

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

        self.v(node.expr)

    def visitAugAssign(self, node):

        self.v(node.node)
        self.v(node.expr)

    def visitCallFunc(self, node):
       #if isinstance(node.node, compiler.ast.Getattr):
       #    pass
       #else:
       #    if not (node.node.name in self.ids['__fn__']):
       #        print node.node.name
                
        self.v(node.node)        

        for i in range(len(node.args)):
            self.v(node.args[i])

            
    def visitCompare(self, node):

        self.v(node.expr)
        for operator, operand in node.ops:
            self.v(operand)

    def visitFunction(self, node):
        self.ids[node.name] = []
        
        self.fn = "__fn__"
        self.addId(node.name)
        
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
   #check = PyCheck()
   #check.check("api.py")
   #check.check("etest.py")
    #print vi.ids
    string = loopFix(open("etest.py").read(), "tester()") 
    print string
    print loopFix("""def main():
    while 1:
        TextOut(0, LCD_LINE1, "socialny defekt")
        Wait(2000)""", "t()")
    print loopFix(open("files/whiletester.py").read(), "tester()")
    #print realLine(string, 30)
