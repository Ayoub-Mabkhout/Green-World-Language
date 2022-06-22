
import sys
sys.path.append('../')
from Lexer.lexer import *



file = path+"OutputFiles/token_stream.txt"
out_folder = path+"OutputFiles/"
# Different from the original Lexer
# this Lexer class has only one method lex()
# which gets the next token from the token stream file


class TokenLexer:
    def __init__(self, filename):
        global tokens
        self.token_stream = open(filename, "r")
        self.curr_token_type = None
        self.curr_token_value = None
        self.line = 0
        self.curr_token = None
        self.iterator = iter(tokens)
    # lex() should raise an InvalidInputError somewhere

    def lex(self):
        global tokens
        self.line += 1
        line = self.token_stream.readline().strip()
        if line == "":
            self.curr_token_type = None
            return
        self.curr_token_type = line.split(" ")[2]
        self.curr_token_value = line.split(
            " ")[3] if len(line.split(" ")) == 4 else None
        self.curr_token = next(self.iterator)
        print(f'TOKEN: {self.curr_token}')
        self.curr_token_type = self.curr_token.tokenType
        self.curr_token_value = self.curr_token.tokenValue


class InvalidInputError(Exception):
    def __init__(self, line, token):
        self.token = token
        self.line = line
        self.message = f'Invalid Input Error in line {self.line} with token {self.token}'
        super().__init__(self.message)


class InvalidSyntaxError(Exception):
    def __init__(self, line, token):
        self.line = line
        self.token = token
        self.message = f'Invalid Syntax Error in line {self.line} with token {self.token}'
        super().__init__(self.message)


class Node:
    def __init__(self, type, val, depth):
        self.depth = depth
        self.type = type
        self.val = val
        self.child = [] if type != "terminal" else None

    def __repr__(self):
        s = self.val
        if self.type == "terminal":
            return str(s) + "\n"
        for node in self.child:
            if self.child.index(node) != 0:
                s += "   "
                for i in range(0, self.depth):
                    s += "        "
            s = s + " --- " + node.__repr__()
        return s


class TerminalNode(Node):
    def __init__(self, type, val, depth, token):
        self.token = token
        super().__init__(type, val, depth)


CST = []


def printCST():
    for node in CST:
        print(
            f'Node: {node.type} {node.val}' if node != None else f'NONE NODE')


def append(node1, node2):
    if node2 == None:
        # print(f'None child node at {node1.val}')
        return
    if node1 == None:
        # print(f'None parent node at {node2.val}')
        return
    node1.child.append(node2)
    CST.append(node2)
    # print(f'append {node2.val} to {node1.val}')
    # print statements commented out were used for debugging


class Parser:
    def __init__(self, filename):
        print("\n\n")
        print("--------------------------------------")
        print("--------- Initializing Parser --------")
        print("--------------------------------------")
        print("\n\n")
        self.TokenLexer = TokenLexer(filename)
        self.run()
        self.root_node

    def run(self):
        self.TokenLexer.lex()
        try:
            self.root_node = self.lang(0)
        except InvalidInputError as e:
            printCST()
            print(e.message)
            sys.exit()
        except InvalidSyntaxError as e:
            printCST()
            print(e.message)
            sys.exit()

    def lang(self, depth):
        n = Node("non-terminal", "LAN", depth)

        c = self.program(depth+1)
        append(n, c)
        if self.TokenLexer.curr_token_type != None:
            print(
                f'Not none token at then end?? {self.TokenLexer.curr_token_type}')
        return n

    def expression(self, depth):
        n = Node("non-terminal", "<E>", depth)

        c = self.term(depth+1)
        append(n, c)
        if(self.TokenLexer.curr_token_type != "ADD_OP"):
            return n
        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        c = self.expression(depth+1)
        append(n, c)
        return n

    def term(self, depth):
        n = Node("non-terminal", "<T>", depth)

        c = self.factor(depth+1)
        append(n, c)
        if(self.TokenLexer.curr_token_type != "MULT_OP"):
            return n
        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        c = self.term(depth+1)
        append(n, c)
        return n

    def factor(self, depth):
        n = Node("non-terminal", "<F>", depth)

        if self.TokenLexer.curr_token_type == "LPAREN":
            c = TerminalNode(
                "terminal", "(", depth+1, self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()
            c = self.expression(depth+1)
            append(n, c)
            if self.TokenLexer.curr_token_type != "RPAREN":
                raise InvalidSyntaxError(
                    self.TokenLexer.line, self.TokenLexer.curr_token_type)
            c = TerminalNode("terminal", ")", depth+1,
                             self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()
            return n

        c = self.value(depth+1)
        append(n, c)
        return n

    def value(self, depth):
        n = Node("non-terminal", "<V>", depth)
        if self.TokenLexer.curr_token_type == None:
            return n
            # still need some way to check if the identifier has been declared previously or not
        if self.TokenLexer.curr_token_type not in ("IDENT", "NUM_LIT", "FRAC_LIT", "FUNC_CALL",
                                                   "QNT", "PRIMITIVE_DIM"):
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)
        if self.TokenLexer.curr_token_type == "FUNC_CALL":
            c = self.functionCall(depth+1)
        else:
            c = TerminalNode(
                "terminal", self.TokenLexer.curr_token_value, depth+1, self.TokenLexer.curr_token)
            self.TokenLexer.lex()
        append(n, c)
        return n

    def boolExpression(self, depth):
        n = Node("non-terminal", "BLE", depth)
        c = self.boolTerm(depth+1)
        append(n, c)

        if self.TokenLexer.curr_token_type != "OR_OP":
            return n

        c = TerminalNode("terminal", "|", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        c = self.boolExpression(depth+1)
        append(n, c)
        return n

    def boolTerm(self, depth):
        n = Node("non-terminal", "BLT", depth)
        c = self.boolFactor(depth+1)
        append(n, c)

        if self.TokenLexer.curr_token_type != "AND_OP":
            return n

        c = TerminalNode("terminal", "&", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        c = self.boolTerm(depth+1)
        append(n, c)
        return n

    def boolFactor(self, depth):
        n = Node("non-terminal", "BLF", depth)

        if self.TokenLexer.curr_token_type == "NOT_OP":
            c = TerminalNode("terminal", "NOT", depth+1,
                             self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()
            c = self.boolFactor(depth+1)
            return n

        if self.TokenLexer.curr_token_type == "LPAREN":
            c = TerminalNode(
                "terminal", "(", depth+1, self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()
            c = self.boolExpression(depth+1)
            append(n, c)
            if self.TokenLexer.curr_token_type == "RPAREN":
                c = TerminalNode("terminal", ")", depth+1,
                                 self.TokenLexer.curr_token)
                append(n, c)
                self.TokenLexer.lex()
                return n
            else:
                raise InvalidSyntaxError(
                    self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = self.comparison(depth+1)
        append(n, c)
        return n

    def comparison(self, depth):
        n = Node("non-terminal", "CMP", depth)

        c = self.expression(depth+1)
        append(n, c)

        if self.TokenLexer.curr_token_type != "COMP_OP":
            return n

        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.comparison(depth+1)
        append(n, c)
        return n

    def assignment(self, depth):
        n = Node("non-terminal", "ASG", depth)

        # need some way to check if the identifier has been declared prior to its use here
        if self.TokenLexer.curr_token_type not in ("IDENT", "PRIMITIVE_DIM", "QNT"):
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        # print(f'DEBUG: CURRENT TOKEN IS {self.TokenLexer.curr_token_type}')
        if self.TokenLexer.curr_token_type != "ASSIGN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)
        c = TerminalNode("terminal", "::", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        c = self.expression(depth+1)
        append(n, c)
        return n

    # only if then else, no else if implementation for now #TBD
    def selection(self, depth):
        n = Node("non-terminal", "SEL", depth)

        if self.TokenLexer.curr_token_type != "IF":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "if", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "(", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.boolExpression(depth+1)
        append(n, c)

        if self.TokenLexer.curr_token_type != "RPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", ")", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "THEN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "THEN", depth+1,
                         self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LCBRACKET":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "{", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.codeBlock(depth+1)
        if c:
            append(n, c)

        if self.TokenLexer.curr_token_type != "RCBRACKET":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "}", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type == "ELSE":
            c = TerminalNode("terminal", "ELSE", depth+1,
                             self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()

            if self.TokenLexer.curr_token_type != "LCBRACKET":
                raise InvalidSyntaxError(
                    self.TokenLexer.line, self.TokenLexer.curr_token_type)

            c = TerminalNode(
                "terminal", "{", depth+1, self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()

            c = self.codeBlock(depth+1)
            if c:
                append(n, c)

            if self.TokenLexer.curr_token_type != "RCBRACKET":
                raise InvalidSyntaxError(
                    self.TokenLexer.line, self.TokenLexer.curr_token_type)

            c = TerminalNode("terminal", "}", depth+1,
                             self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()

        return n

    def jumpStmt(self, depth):
        n = Node("non-terminal", "JMP", depth)

        if self.TokenLexer.curr_token_type == "RETURN":
            c = TerminalNode("terminal", "return", depth +
                             1, self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()
            c = self.expression(depth+1)
            append(n, c)
        elif self.TokenLexer.curr_token_type == "LOOP":
            c = self.loop(depth+1)
            append(n, c)
        else:
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)
        return n

    def loop(self, depth):
        n = Node("non-terminal", "LOP", depth)

        if self.TokenLexer.curr_token_type != "LOOP":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)
        c = TerminalNode("terminal", "loop", depth+1,
                         self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)
        c = TerminalNode("terminal", "(", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.boolExpression(depth+1)
        append(n, c)

        if self.TokenLexer.curr_token_type != "RPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)
        c = TerminalNode("terminal", ")", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LCBRACKET":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)
        c = TerminalNode("terminal", "{", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.codeBlock(depth+1)
        if c:
            append(n, c)

        if self.TokenLexer.curr_token_type != "RCBRACKET":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)
        c = TerminalNode("terminal", "}", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        return n

    def functionCall(self, depth):
        n = Node("non-terminal", "FNC", depth)

        if self.TokenLexer.curr_token_type != "FUNC_CALL":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "call", depth+1,
                         self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type not in ("IDENT", "PRIMITIVE_FUNC"):
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "TAKE":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "take", depth+1,
                         self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "(", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.arguments(depth+1)
        if c:
            append(n, c)

        if self.TokenLexer.curr_token_type != "RPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", ")", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        return n

    def variableDec(self, depth):
        n = Node("non_terminal", "DEC", depth)

        # if self.TokenLexer.curr_token_type != "VAR_DEC":
        #     raise InvalidSyntaxError(
        #         self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "Dec", depth+1,
                         self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.type(depth+1)
        append(n, c)

        if self.TokenLexer.curr_token_type != "IDENT":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        return n

    def type(self, depth):
        n = Node("non-terminal", "TYP", depth)

        if self.TokenLexer.curr_token_type not in ("PRIMITIVE_TYPE", "PRIMITIVE_STRUCT"):
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()
        return n

    def statement(self, depth):
        n = Node("non-terminal", "STM", depth)
        need_end = False

        if self.TokenLexer.curr_token_type in ("LOOP", "RETURN"):
            if self.TokenLexer.curr_token_type == "RETURN":
                need_end = True
            c = self.jumpStmt(depth+1)
        elif self.TokenLexer.curr_token_type == "IF":
            c = self.selection(depth+1)
        elif self.TokenLexer.curr_token_type == "VAR_DEC":
            c = self.variableDec(depth+1)
            need_end = True
        elif self.TokenLexer.curr_token_type == "FUNC_CALL":
            c = self.functionCall(depth+1)
            need_end = True
        elif self.TokenLexer.curr_token_type in ("IDENT", "PRIMITIVE_DIM", "QNT"):
            c = self.assignment(depth+1)
            need_end = True
        else:
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        append(n, c)

        if need_end:
            if self.TokenLexer.curr_token_type != "END":
                raise InvalidSyntaxError(
                    self.TokenLexer.line, self.TokenLexer.curr_token_type)

            c = TerminalNode("terminal", ";", depth+1,
                             self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()

        return n

    def arguments(self, depth):
        n = Node("non-terminal", "ARG", depth)
        if self.TokenLexer.curr_token_type == "RPAREN":
            return None

        c = self.expression(depth+1)
        append(n, c)

        while self.TokenLexer.curr_token_type == "COMMA":
            c = TerminalNode("terminal", ",", depth+1,
                             self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()

            c = self.expression(depth+1)
            append(n, c)

        return n

    def codeBlock(self, depth):
        n = Node("non-terminal", "TCB", depth)
        if self.TokenLexer.curr_token_type == "RCBRACKET":
            return None

        while self.TokenLexer.curr_token_type != "RCBRACKET":
            c = self.statement(depth+1)
            append(n, c)
        return n

    def mainFunction(self, depth):
        n = Node("non-terminal", "MNF", depth)

        if self.TokenLexer.curr_token_type != "MAIN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "Main", depth+1,
                         self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type, self.TokenLexer.curr_token)

        c = TerminalNode("terminal", "(", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "RPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", ")", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LCBRACKET":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "{", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.codeBlock(depth+1)
        if c:
            append(n, c)

        if self.TokenLexer.curr_token_type != "RCBRACKET":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "}", depth+1, self.TokenLexer.curr_token)
        self.TokenLexer.lex()

        return n

    def functionDef(self, depth):
        n = Node("non-terminal", "FND", depth)

        c = TerminalNode("terminal", "Def", depth+1,
                         self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.type(depth+1)
        append(n, c)

        if self.TokenLexer.curr_token_type != "IDENT":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "(", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.parameters(depth+1)
        if c:
            append(n, c)

        if self.TokenLexer.curr_token_type != "RPAREN":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", ")", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "LCBRACKET":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "{", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.codeBlock(depth+1)
        if c:
            append(n, c)

        if self.TokenLexer.curr_token_type != "RCBRACKET":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", "}", depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        return n

    def parameters(self, depth):
        n = Node("non-terminal", "PAR", depth)
        if self.TokenLexer.curr_token_type == "RPAREN":
            return None

        c = self.type(depth+1)
        append(n, c)

        if self.TokenLexer.curr_token_type != "IDENT":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        while self.TokenLexer.curr_token_type == "COMMA":
            c = TerminalNode("terminal", ",", depth+1,
                             self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()

            c = self.type(depth+1)
            append(n, c)

            if self.TokenLexer.curr_token_type != "IDENT":
                raise InvalidSyntaxError(
                    self.TokenLexer.line, self.TokenLexer.curr_token_type)

            c = TerminalNode(
                "terminal", self.TokenLexer.curr_token_value, depth+1, self.TokenLexer.curr_token)
            append(n, c)
            self.TokenLexer.lex()
        return n

    def constantDef(self, depth):
        n = Node("non-terminal", "CST", depth)

        c = TerminalNode("terminal", "$CONST", depth +
                         1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        if self.TokenLexer.curr_token_type != "IDENT":
            raise InvalidSyntaxError(
                self.TokenLexer.line, self.TokenLexer.curr_token_type)

        c = TerminalNode("terminal", self.TokenLexer.curr_token_value,
                         depth+1, self.TokenLexer.curr_token)
        append(n, c)
        self.TokenLexer.lex()

        c = self.expression(depth+1)
        append(n, c)

        return n

    def program(self, depth):
        n = Node("non-terminal", "PRG", depth)

        while self.TokenLexer.curr_token_type != "MAIN":
            need_end = False
            if self.TokenLexer.curr_token_type == "CONST_DEF":
                c = self.constantDef(depth+1)
            elif self.TokenLexer.curr_token_type == "FUNC_DEF":
                c = self.functionDef(depth+1)
            elif self.TokenLexer.curr_token_type == "VAR_DEC":
                c = self.variableDec(depth+1)
                need_end = True
            elif self.TokenLexer.curr_token_type in ("IDENT", "PRIMITIVE_DIM", "QNT"):
                c = self.assignment(depth+1)
                need_end = True
            else:
                raise InvalidSyntaxError(
                    self.TokenLexer.line, self.TokenLexer.curr_token_type)

            append(n, c)

            if need_end:
                if self.TokenLexer.curr_token_type != "END":
                    raise InvalidSyntaxError(
                        self.TokenLexer.line, self.TokenLexer.curr_token_type)

                c = TerminalNode("terminal", ";", depth+1,
                                 self.TokenLexer.curr_token)
                append(n, c)
                self.TokenLexer.lex()

        c = self.mainFunction(depth+1)
        append(n, c)

        return n



parser = Parser(file)
# print(parser.root_node)
with open(out_folder+"CST.txt", "w") as f:
    f.write(parser.root_node.__repr__())
printCST()
