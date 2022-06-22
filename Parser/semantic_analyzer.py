import sys
sys.path.append('../')
from Parser.parse import CST,symbol_table,Token,path

import traceback
import logging
out_folder = path+"OutputFiles/"
root = None
AST = []
longest = 0
current_scope = "global"
local_scope_content = []
global_scope_content = []
countor = 0


class RootNode:
    def __init__(self, depth):
        self.depth = depth
        self.val = "PRG"
        self.operands = []
        AST.append(self)
        global longest
        if(len(self.val) > longest):
            longest = len(self.val)

    def __repr__(self):
        s = self.val
        if not self.operands:
            return s + "\n"
        for op in self.operands:
            sa = ""
            if self.operands.index(op) != 0:
                for i in range(self.depth):
                    s += " " * (longest+5)
                sa += " " * (len(self.val) + 0)
            sa += " " + "-" * (longest-len(self.val)+3) + " "
            s += sa
            s += op.__repr__()
        return s


class OperandNode(RootNode):
    def __init__(self, value, depth, token):
        super().__init__(depth)
        self.val = value
        self.operands = None
        self.token = token


class ASTNode(RootNode):
    def __init__(self, value, depth, token):
        super().__init__(depth)
        self.val = value
        self.token = token


class ReachTerminalNodeError(Exception):
    def __init__(self, production):
        self.message = f'Should not have reached terminal node {production.val}'
        super().__init__(self.message)


class InvalidParseTreeError(Exception):
    def __init__(self, production):
        self.message = f'Invalid Parse Tree Error at production: {production.__dict__}'
        super().__init__(self.message)


class SymbolKeyError(Exception):
    def __init__(self, symbol, symbol_table):
        self.message = f'Symbol {symbol} not found in symbol_table with keys:\n{symbol_table.keys()}'
        super().__init__(self.message)


class ReferencedUndeclaredSymbolError(Exception):
    def __init__(self, symbol):
        global symbol_table
        self.message = f'Refereneced {symbol} of category {symbol_table[symbol]["category"]} before declaration'
        super().__init__(self.message)


class ArgumentsNotMatchingError(Exception):
    def __init__(self, symbol, arguments):
        args = []
        for arg in arguments:
            args.append(arg.val)
        self.message = f'arguments: {args} do not match parameters {symbol_table[symbol]["parameters"].keys()}'


class DoubleDeclarationError(Exception):
    def __init__(self, symbol):
        global local_scope_content
        global global_scope_content
        global current_scope
        global symbol_table
        scope_content = local_scope_content if current_scope == "local" else global_scope_content
        self.message = f'Duplicate declaration/definition for {symbol_table[symbol]["category"]} {symbol} in the same scope containing {scope_content}'
        super().__init__(self.message)


def match_arguments(symbol, arguments):
    args = []
    for arg in arguments:
        args.append(arg.val)
        if not isDeclared(arg.val):
            raise ReferencedUndeclaredSymbolError(arg.val)
    print(f'DEBUG: MATCHING ARGUMENTS for function {symbol}')
    print(args)
    print(symbol_table[symbol]["parameters"].keys())
    # if args == symbol_table[symbol]["parameters"].keys():
    if len(args) == len(symbol_table[symbol]["parameters"].keys()):
        return True
    else:
        return False


# initialize global_scope_content


def initialize_gsc():
    for symbol in symbol_table:
        if symbol_table[symbol]["category"] in ("variable", "constant"):
            if symbol_table[symbol]["scope"] == "global":
                global_scope_content.append(symbol)


def declare_var(symbol):
    global current_scope
    global local_scope_content
    global global_scope_content
    global symbol_table

    symbol = symbol.rstrip("\n")
    if isDeclared(symbol):
        raise DoubleDeclarationError(symbol)

    symbol_table[symbol]["category"] = "variable"
    symbol_table[symbol]["scope"] = current_scope
    if current_scope == "local":
        local_scope_content.append(symbol)
    else:
        global_scope_content.append(symbol)


def define_cst(symbol):
    global current_scope
    global local_scope_content
    global global_scope_content
    global symbol_table

    symbol = symbol.rstrip("\n")
    if isDeclared(symbol):
        raise DoubleDeclarationError(symbol)

    symbol_table[symbol]["category"] = "constant"
    symbol_table[symbol]["scope"] = current_scope
    global_scope_content.append(symbol)


def define_fun(symbol, parameters):
    global current_scope
    global local_scope_content
    global symbol_table

    if symbol not in symbol_table.keys():
        raise SymbolKeyError(symbol, symbol_table)

    if isDeclared(symbol):
        raise DoubleDeclarationError(symbol)

    symbol_table[symbol]["category"] = "function"
    symbol_table[symbol]["scope"] = "global"
    pars = {}

    for par in parameters:
        pars[par.operands[0].val] = par.val

    symbol_table[symbol]["parameters"] = pars
    parameters_list = list(pars.keys())

    for key in parameters_list:
        declare_var(key)
        local_scope_content.append(key)

    global_scope_content.append(symbol)


def isDeclared(symbol):
    # this function can also take other types of arguments that might not be present in the symbol table
    # these should be ignored and the function should return true
    if symbol not in symbol_table.keys():
        return True
    scope = symbol_table[symbol]["scope"]
    if not scope:
        return False
    elif scope == "global":
        return True
    else:
        if symbol in local_scope_content or symbol in global_scope_content:
            return True
        else:
            return False


def get_PRG_actions(production, depth):
    actions = []
    for node in production.child:
        if node.val != ";":
            actions.append(get_operand(node, depth))
    return actions


def get_operand(production, depth):
    node = None
    global current_scope
    global local_scope_content
    global countor

    countor += 1

    if production.type == "terminal":
        # raise ReachTerminalNodeError(production)
        node = OperandNode(production.val, depth, production.token)

    elif production.val == "PRG":

        actions = get_PRG_actions(production, depth+1)
        node = RootNode(depth)
        node.operands = actions.copy()

    elif production.val == "MNF":
        local_scope_content = []
        current_scope = "local"
        operator = get_operand(production.child[0], depth)
        actions = get_operand(production.child[4], depth+1)
        node = ASTNode(operator.val, depth, operator.token)
        node.operands = actions.copy()

    elif production.val == "TCB":
        node = []
        for n in production.child:
            node.append(get_operand(n, depth))

    elif production.val in ("STM", "V"):
        node = get_operand(production.child[0], depth)

    elif production.val == "ASG":
        operator = get_operand(production.child[1], depth)
        left_operand = get_operand(production.child[0], depth+1)
        if not isDeclared(left_operand.val):
            raise ReferencedUndeclaredSymbolError(left_operand.val)
        right_operand = get_operand(production.child[2], depth+1)
        node = ASTNode(operator.val, depth, operator.token)
        node.operands.append(left_operand)
        node.operands.append(right_operand)

    elif production.val in ("<E>", "<T>", "BLE", "BLT", "CMP"):
        if len(production.child) == 3:
            operator = get_operand(production.child[1], depth)
            left_operand = get_operand(production.child[0], depth+1)
            if not isDeclared(left_operand.val):
                raise ReferencedUndeclaredSymbolError(left_operand.val)
            right_operand = get_operand(production.child[2], depth+1)
            if not isDeclared(right_operand.val):
                raise ReferencedUndeclaredSymbolError(right_operand.val)
            node = ASTNode(operator.val, depth, operator.token)
            node.operands.append(left_operand)
            node.operands.append(right_operand)
        else:
            node = get_operand(production.child[0], depth)

    elif production.val == "<F>":
        if production.child[0].val == '(':
            node = get_operand(production.child[1], depth)
        else:
            node = get_operand(production.child[0], depth)

    elif production.val in ("<V>", "TYP"):
        node = get_operand(production.child[0], depth)

    elif production.val == "BLF":
        if production.child[0].val == "NOT":
            operator = get_operand(production.child[0], depth)
            operand = get_operand(production.child[1], depth+1)
            node = ASTNode(operator.val, depth, operator.token)
            node.operands.append(operand)
        elif production.val == "(":
            node = get_operand(production.child[1], depth)
        else:
            node = get_operand(production.child[0], depth)

    elif production.val == "LOP":
        operator = get_operand(production.child[0], depth)
        condition = get_operand(production.child[2], depth+1)
        body = get_operand(production.child[5], depth+1)
        node = ASTNode(operator.val, depth, operator.token)
        node.operands.append(condition)
        node.operands += body

    elif production.val == "SEL":
        operator = get_operand(production.child[0], depth)
        condition = get_operand(production.child[2], depth+1)
        then_kw = get_operand(production.child[4], depth+1)
        then_body = get_operand(production.child[6], depth+2)
        then_kw.operands = then_body.copy()
        else_kw = None
        if len(production.child) > 10:
            else_kw = get_operand(production.child[8], depth+1)
            else_body = get_operand(production.child[10], depth+2)
            else_kw.operands = else_body.copy()
        node = ASTNode(operator.val, depth, operator.token)
        node.operands.append(then_kw)
        if else_kw:
            node.operands.append(else_kw)

    elif production.val == "DEC":
        operator = get_operand(production.child[0], depth)
        type = get_operand(production.child[1], depth+1)
        var = get_operand(production.child[2], depth+1)
        node = ASTNode(operator.val, depth, operator.token)
        node.operands.append(type)
        node.operands.append(var)
        declare_var(var.val)

    elif production.val == "JMP":
        if len(production.child) == 1:
            node = get_operand(production.child[0], depth)
        else:
            operator = get_operand(production.child[0], depth)
            operand = get_operand(production.child[1], depth+1)
            node = ASTNode(operator.val, depth, operator.token)
            node.operands.append(operand)

    elif production.val == "FND":
        local_scope_content = []
        current_scope = "local"
        operator = get_operand(production.child[0], depth)
        type = get_operand(production.child[1], depth+1)
        name = get_operand(production.child[2], depth+1)
        parameters = get_operand(production.child[4], depth+1)
        define_fun(name.val, parameters)
        body = get_operand(production.child[7], depth+1)
        node = ASTNode(operator.val, depth, operator.token)
        node.operands.append(type)
        node.operands += parameters
        node.operands += body

        current_scope = "global"

    elif production.val == "PAR":
        nodes = []
        for i in range(0, len(production.child), 3):
            type = get_operand(production.child[i], depth)
            name = get_operand(production.child[i+1], depth+1)
            node = ASTNode(type.val, depth, type.token)
            node.operands.append(name)
            nodes.append(node)
        return nodes

    elif production.val == "FNC":
        operator = get_operand(production.child[0], depth)
        name = get_operand(production.child[1], depth+1)
        if not isDeclared(name.val):
            raise ReferencedUndeclaredSymbolError(name.val)
        take_kw = get_operand(production.child[2], depth+1)
        take = ASTNode(take_kw.val, depth+1, operator.token)
        arguments = get_operand(production.child[4], depth+2)
        if not match_arguments(name.val, arguments):
            raise ArgumentsNotMatchingError(name.val, arguments)
        node = ASTNode(operator.val, depth, operator.token)
        node.operands.append(name)
        take.operands += arguments
        node.operands.append(take)

    elif production.val == "ARG":
        nodes = []
        for i in range(0, len(production.child), 2):
            node = get_operand(production.child[i], depth)
            if not isDeclared(node.val):
                raise ReferencedUndeclaredSymbolError(node.val)
            nodes.append(node)
        return nodes

    elif production.val == "CST":
        operator = get_operand(production.child[0], depth)
        cst = get_operand(production.child[1], depth+1)
        value = get_operand(production.child[2], depth+1)
        node = ASTNode(operator.val, depth, operator.token)
        node.operands.append(cst)
        node.operands.append(value)
        define_cst(cst.val)

    else:
        raise InvalidParseTreeError(production)
    return node


def printAST():
    for node in AST:
        print(f'{type(node).__name__}')
        print(f'{node.__dict__}')


def print_st():
    text = "----------- Symbol Table ------------\n\n"
    for key, value in symbol_table.items():
        text += str(key) + ' : ' + str(value) + "\n"
    text += "-------------------------------------\n\n"
    return text


def run(CST):
    global symbol_table
    global root
    filename = "symbols.txt"
    print("\n\n")
    print("--------------------------------------")
    print("--- Initializing Semantic Analyzer ---")
    print("--------------------------------------")
    print("\n\n")
    try:
        initialize_gsc()
        print("initial keys: ", symbol_table.keys())
        root = get_operand(CST.pop(), 0)
    except ReachTerminalNodeError as e:
        printAST()
        print(e.message)
        exit()
    except ArgumentsNotMatchingError as e:
        print(e.message)
        exit()
    except InvalidParseTreeError as e:
        printAST()
        print(e.message)
        exit()
    except SymbolKeyError as e:
        print(e.message)
        exit()
    except ReferencedUndeclaredSymbolError as e:
        print(e.message)
        exit()
    except DoubleDeclarationError as e:
        print(e.message)
        exit()
    except Exception as e:
        printAST()
        logging.error(traceback.format_exc())
        exit()
    finally:
        print(print_st())
        print(global_scope_content)
        print(local_scope_content)

    print("\n\n")
    print("--------------------------------------")
    print("------ Reached End Successfully ------")
    print("--------------------------------------")
    print("\n\n")

    with open(out_folder+"AST.txt", "w+") as f:
        f.write(root.__repr__())
    with open(out_folder+"symbol_table.txt","w+") as f:
        f.write(print_st())


run(CST)
