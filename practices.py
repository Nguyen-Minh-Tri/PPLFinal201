from CodeGenerator import *

#de 18 -- visitDowhile

def visitDowhile(self, ast, c):
    c.frame.enterLoop()
    subBody = SubBody(c.frame, c.sym)
    self.emit.printout(self.emit.emitLABLE(c.frame.getContinueLabel(), c.frame))
    expCode, _ = ast.exp.accept(self, Access(c.frame, c.sym))
    list(map(lambda element: element.accept(self, subBody), ast.sl[0] + ast.sl[1]))
    self.emit.printout(expCode)
    self.emit.printout(self.emit.emitIFTRUE(c.frame.getContinueLAbel(), c.frame))
    self.emit.printout(self.emit.emitLABEL(c.frame.getBreakLabel(), c.frame))
    c.frame.exitLoop()


#de 17 -- visitFor

def visitFor(self, ast, c):
    #preparing before enter emiting
    #########################################
    c.frame.enterLoop()
    subBody = SubBody(c.fame, c.sym)

    #########################################
    #khong co idx1 nhung ma viet luon cho giong ass4

    idRCode, _ = ast.idx1.accept(self, Access(c.frame, c.sym))
    idWCode, _ = ast.idx1.accept(self, Access(c.frame, c.sym, True))
    expr1Code, _ = ast.expr1.accept(self, Access(c.frame, c.sym))
    expr2Code, _ = ast.expr1.accept(self, Access(c.frame, c.sym))
    expr3Code, _ = ast.expr3.accept(self, Access(c.frame, c.sym))
    #########################################
    enterLabel = c.frame.getNewLabel() # chi dung trong for, if 
    # thuc ra o day khong can khai bao, dua xuong duoi emit cung duoc nhung dai vl
    #########################################


    #enter emiting -- load code sau do emit code da load
    self.emit.printout(expr1Code)
    self.emit.printout(idWCode)
    self.emit.printout(self.emit.emitGOTO(enterLabel, c.frame))
    self.emit.printout(self.emit.emitLABEL(c.frame.getContinueLabel()))
    self.emit.printout(expr3Code)
    self.emit.printout(idRCode)
    self.emit.printout(self.emit.emitADDOP('+', IntType(), c.frame))
    self.emit.printout(idWCode)
    self.emit.printout(self.emitLABEL(enterLabel, c.frame))
    self.emit.printout(expr2Code)
    self.emit.printout(self.emitLABEL(c.frame.getBreakLabel(), c.frame))

    #chay cai loop
    list(map(lambda element: element.accept(self, subBody), ast.loop[0] + ast.loop[1]))

    #emit tiep cho vong tiep theo bang cach lay vi tri chay va dung vong hien tai
    self.emit.printout(self.emit.emitGOTO(c.frame.getContinueLabel(), c.frame))
    self.emit.printout(self.emit.emitLABEL(c.frame.getBreakLabel(), c.frame))
    c.frame.exitLoop()

#de 17 -- binop 
#cau nay chi yeu cau viet cho AND operator

def visitBinaryOp(self, ast, c):
    # op = ast.op
    leftCode, _ = ast.left.accept(self, Access(c.frame, c.sym))
    rightCode, _ = ast.right.accept(self, Access(c.frame, c.sym))
    code = leftCode + rightCode
    #op must be '&&' check or not is nonsense
    return code + self.emitANDOP(c.frame), BoolType()

def visitBooleanLiteral(self, ast, c):
    return self.emit.emitPUSHICONST(str(ast.value).lower(), c.frame) if c.frame else None, BoolType()

