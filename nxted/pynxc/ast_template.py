#!/usr/bin/env python
__author__  = ''
__version__ = (0,0)

import sys
import compiler.ast
from compiler.visitor import ASTVisitor
from compiler import parse, walk
from compiler.consts import *

class Visitor(ASTVisitor): 
    def __init__(self,stream=sys.stdout,debug=False):
        self.v = lambda tree, visitor=self: walk(tree, visitor)
        self.stream = stream
        self.strcode = ""
        self.debug=debug
        self.indents = 0
        ASTVisitor.__init__(self)

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
        
    def visitBlock(self, block):
        if self.debug:
            print 'visitBlock'

    def visitAdd(self, node):
        if self.debug:
            print 'visitAdd'

    def visitAnd(self, node):
        if self.debug:
            print 'visitAnd'

    def visitAssAttr(self, node):
        if self.debug:
            print 'visitAssAttr'

    def visitAssList(self, node):
        if self.debug:
            print 'visitAssList'

    def visitAssName(self, node):
        if self.debug:
            print 'visitAssName'
            if node.flags == OP_DELETE:
                print "del ",
            print node.name
        

    def visitAssTuple(self, node):
        if self.debug:
            print 'visitAssTuple'

    def visitAssert(self, node):
        if self.debug:
            print 'visitAssert'

    def visitAssign(self, node):
        if self.debug:
            print 'visitAssign'
        for i in range(len(node.nodes)):
            n = node.nodes[i]
            if self.debug:
                print "  Node ",n
            self.v(n)
        self.v(node.expr)

    def visitAugAssign(self, node):
        if self.debug:
            print 'visitAugAssign'
        self.v(node.node)
        self.v(node.expr)

    def visitBackquote(self, node):
        if self.debug:
            print 'visitBackquote'

    def visitBitand(self, node):
        if self.debug:
            print 'visitBitand'

    def visitBitor(self, node):
        if self.debug:
            print 'visitBitor'

    def visitBitxor(self, node):
        if self.debug:
            print 'visitBitxor'

    def visitBreak(self, node):
        if self.debug:
            print 'visitBreak'

    def visitCallFunc(self, node):
        if self.debug:
            print 'visitCallFunc'
            print 'funcname: ',node.node.name
            
            
        self.v(node.node)
        for i in range(len(node.args)):
            self.v(node.args[i])

            
            
            
    def visitClass(self, node):
        if self.debug:
            print 'visitClass'

    def visitCompare(self, node):
        if self.debug:
            print 'visitCompare'
        self.v(node.expr)
        for operator, operand in node.ops:
            self.v(operand)

    def visitConst(self, node):
        if self.debug:
            print 'visitConst'
            print "Const",repr(node.value)

    def visitContinue(self, node):
        if self.debug:
            print 'visitContinue'

    def visitDecorators(self, node):
        if self.debug:
            print 'visitDecorators'

    def visitDict(self, node):
        if self.debug:
            print 'visitDict'

    def visitDiscard(self, node):
        if self.debug:
            print 'visitDiscard'
        self.v(node.expr)

    def visitDiv(self, node):
        if self.debug:
            print 'visitDiv'

    def visitFloorDiv(self, node):
        if self.debug:
            print 'visitFloorDiv'

    def visitEllipsis(self, node):
        if self.debug:
            print 'visitEllipsis'

    def visitExec(self, node):
        if self.debug:
            print 'visitExec'

    def visitFor(self, node):
        if self.debug:
            print 'visitFor'

    def visitFrom(self, node):
        if self.debug:
            print 'visitFrom'

    def visitFunction(self, node):
        if self.debug:
            print 'visitFunction'
        self.v(node.code)

    def visitGenExpr(self, node):
        if self.debug:
            print 'visitGenExpr'

    def visitGenExprFor(self, node):
        if self.debug:
            print 'visitGenExprFor'

    def visitGetattr(self, node):
        if self.debug:
            print 'visitGetattr'

    def visitGlobal(self, node):
        if self.debug:
            print 'visitGlobal'

    def visitIf(self, node):
        if self.debug:
            print 'visitIf'
            
        (c, b) = node.tests[0]
        self.v(c)
        self.v(b)
    
        for c, b in node.tests[1:]:
            self.v(c)
            self.v(b)
        if node.else_:
            self.v(node.else_)

    def visitImport(self, node):
        if self.debug:
            print 'visitImport'

    def visitInvert(self, node):
        if self.debug:
            print 'visitInvert'

    def visitKeyword(self, node):
        if self.debug:
            print 'visitKeyword'
        self.v(node.expr)

    def visitLambda(self, node):
        if self.debug:
            print 'visitLambda'

    def visitLeftShift(self, node):
        if self.debug:
            print 'visitLeftShift'

    def visitList(self, node):
        if self.debug:
            print 'visitList'

    def visitListComp(self, node):
        if self.debug:
            print 'visitListComp'

    def visitListCompFor(self, node):
        if self.debug:
            print 'visitListCompFor'

    def visitListCompIf(self, node):
        if self.debug:
            print 'visitListCompIf'

    def visitMod(self, node):
        if self.debug:
            print 'visitMod'

    def visitModule(self, node):
        if self.debug:
            print 'visitModule'
        self.v(node.node)

    def visitMul(self, node):
        if self.debug:
            print 'visitMul'

    def visitName(self, node):
        if self.debug:
            print 'visitName'
            print "Name",node.name

    def visitNot(self, node):
        if self.debug:
            print 'visitNot'

    def visitOr(self, node):
        if self.debug:
            print 'visitOr'

    def visitPass(self, node):
        if self.debug:
            print 'visitPass'

    def visitPower(self, node):
        if self.debug:
            print 'visitPower'

    def visitPrint(self, node):
        if self.debug:
            print 'visitPrint'

    def visitPrintnl(self, node):
        if self.debug:
            print 'visitPrintnl'

    def visitRaise(self, node):
        if self.debug:
            print 'visitRaise'

    def visitReturn(self, node):
        if self.debug:
            print 'visitReturn'

    def visitRightShift(self, node):
        if self.debug:
            print 'visitRightShift'

    def visitSlice(self, node):
        if self.debug:
            print 'visitSlice'

    def visitStmt(self, node):
        if self.debug:
            print 'visitStmt'
        for n in node.nodes:
            self.v(n)

    def visitSub(self, node):
        if self.debug:
            print 'visitSub'

    def visitSubscript(self, node):
        if self.debug:
            print 'visitSubscript'

    def visitTryExcept(self, node):
        if self.debug:
            print 'visitTryExcept'

    def visitTryFinally(self, node):
        if self.debug:
            print 'visitTryFinally'

    def visitTuple(self, node):
        if self.debug:
            print 'visitTuple'

    def visitUnaryAdd(self, node):
        if self.debug:
            print 'visitUnaryAdd'

    def visitUnarySub(self, node):
        if self.debug:
            print 'visitUnarySub'

    def visitWhile(self, node):
        if self.debug:
            print 'visitWhile'
        self.v(node.test)
        self.v(node.body)
        if node.else_:
            self.v(node.else_)

    def visitYield(self, node):
        if self.debug:
            print 'visitYield'


        
def ast2py(ast,debug=True):
    v = Visitor(debug)
    v.v(ast)
    return str(v)

def main():
    filename = 'test.py'
    ast = parse(open(filename).read())
    s = ast2py(ast)
    return s

if __name__ == "__main__":
    print main()
