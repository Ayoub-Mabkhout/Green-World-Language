import hashlib
import sys
sys.path.append('../')
from Parser.semantic_analyzer import AST, global_scope_content, symbol_table, root, Token,path

WIDTH, DEPTH, HEIGHT = 20, 20, 10
qnt_blocks, qnt_tubs, qnt_earth, qnt_plants = 30, 22, 13, 8
ident_dic = {}
data_definitions = []
instructions = []
# current scope is either 'global' or is the name of the function inside
current_scope = 'global'
# of which the scope is being considered

out_folder = path + "OutputFiles/"
filename = out_folder + "assembly.txt"

# we will use generate and use a dictionary
# to assign labels to to function calls or to identifiers

# in GWL, identifier values may not match the restrictions put on labels in GWAL
# meaning that we cannot use identifiers directly as labels.
# since the code generation has to be methodical and automatic
# we cannot really afford to have descriptive names for labels
# so 7-character long labels we be generated automatically from hashing identifiers
# the identifiers and their labels will be stored in a dictionary
# as key-value pairs, some labels might also take suffixes in cases
# where an identifier of some type might need multiple labels to represent it in GWAL


# we will have a DataDefLine class and an InstructionLine class
# as well as lists to would hold all DataDefinitions and all Instructions

# the AST will be read DFS and the deepest leftmost opNodes will be
# converted into GWAL instructions or data definitions
# before their parent opNodes

# our GWAL code will use a number of temporary variables
# sort of like registries

class TooLongEntryError(Exception):
    def __init__(self, entry, line):
        self.message = f'Error: Entry \"{entry}\" too long in line:\n{line}'
        super().__init__(self.message)


def check_args(args, line):
    for arg in args:
        if len(arg) > 9:
            raise TooLongEntryError(arg, line)


class DataDefLine:
    def __init__(self, var_const, udi, type, size, value):
        self.var_const = var_const
        self.udi = udi
        self.type = type
        self.size = size
        self.value = value
        check_args([self.var_const, self.udi,
                   self.type, self.size, self.value], self)

    def __repr__(self):
        return f'{self.var_const}\t{self.udi}\t{self.type}\t{self.size}\t{self.value}\n'


class LongString(DataDefLine):
    def __init__(self, content):
        self.content = content
        if len(content) > 49:
            raise TooLongEntryError(content, self)
        super().__init__("", "", "", "", "")

    def __repr__(self):
        return self.content + "\n"


class InstructionLine:
    def __init__(self, label, operator, operand1, operand2, operand3):
        self.label = label
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
        check_args([self.label, self.operator, self.operand1,
                   self.operand2, self.operand3], self)

    def __repr__(self):
        return f'{self.label}\t{self.operator}\t{self.operand1}\t{self.operand2}\t{self.operand3}\n'


def hash_identifier(ident):
    # this function takes in an identifier and hashes it
    hash_object = hashlib.sReturne_256(ident.encode('UTF-8'))
    hex_hashed = hash_object.hexdigest(6)
    # print(f'hex_hashed is {hex_hashed}')

    hash_string = ""
    for i in range(0, len(hex_hashed), 2):
        hex_val = hex_hashed[i] + hex_hashed[i+1]
        dec_val = int(hex_val, 16)
        char = chr(ord('A')+(dec_val % 26))
        hash_string += (char)
    ident_dic[ident] = hash_string
    return hash_string

# this function uses the lists data_definitions and instructions to write the lines of
# the assembly code into a file


def print_code():
    global data_definitions
    global instructions
    code = "PROGRAM\tgenerated\n## This comment is just here to test comments\nDATA\n\n## This is where you would place DataDefinitions\n"
    for datum in data_definitions:
        code += datum.__repr__()
    code += "\nCODE\n## This is where Executable Instructions go\n"
    for instruction in instructions:
        code += instruction.__repr__()
    with open(filename, "w+") as out:
        out.write(code)
    print(code)


def const_var_line(args):
    id = args[0]
    # print(id)
    var_const = symbol_table[id]["category"]
    if var_const != "function":
        if var_const == "variable":
            var_const = "VAR"
        else:
            var_const = "CONST"
        name = hash_identifier(id)
        # default value will be an int, but the it might be updated
        # during the code generation phase when the type is determined
        # in the declare statement
        if len(args) > 1:
            type = args[1]
        else:
            type = "INT"
        if len(args) > 2:
            size = args[2] 
        else:
            size = ""
        # value might be initialized once an assign statement is detected
        # in the global scope, but at this point it is left empty
        if len(args) > 3:
            value = args[3]
        else:
            value = ""
        line = DataDefLine(var_const, name, type, size, value)
        return line


# temporary
def define_globals():
    global global_scope_content
    data = []
    for id in global_scope_content:
        datum = const_var_line([id])
        data.append(datum)
    return data
# might never use it


def initialize_data_def():
    global data_definitions
    world = DataDefLine("VAR", "WORLD", "INT", str(WIDTH*DEPTH*HEIGHT), "0")
    qblocks_name = hash_identifier("qBlock")
    qtubs_name = hash_identifier("qTub")
    qearth_name = hash_identifier("qEarth")
    qplants_name = hash_identifier("qPlant")
    qblocks = DataDefLine("VAR", qblocks_name, "INT", "1", str(qnt_blocks))
    qtubs = DataDefLine("VAR", qtubs_name, "INT", "1", str(qnt_tubs))
    qearth = DataDefLine("VAR", qearth_name, "INT", "1", str(qnt_earth))
    qplants = DataDefLine("VAR", qplants_name, "INT", "1", str(qnt_plants))
    temp1 = DataDefLine("VAR", "TEMP1", "INT", "", "")
    temp2 = DataDefLine("VAR", "TEMP2", "INT", "", "")
    temp3 = DataDefLine("VAR", "TEMP3", "INT", "", "")
    temp4 = DataDefLine("VAR", "TEMP4", "INT", "", "")
    str_const = DataDefLine("CONST", "TEXT", "STRING", "0", "*")
    str_const_text = LongString(
        "This is supposed to be a constant long string")
    var_name = hash_identifier("var_name")
    variable = DataDefLine("VAR", var_name, "INT", "1", "")

    data_definitions += [world, qblocks, qtubs, qearth, qplants, temp1, temp2, temp3, temp4,
                         str_const, str_const_text, variable]


def traverse(node):
    global current_scope
    global data_definitions
    # print(f'currently visiting node {node.val}')  # print for debugging
    # when reaching an operand node, just return its value
    if not node.operands:
        return node.val
    if node.val == "PRG":
        for operand in node.operands:
            traverse(operand)
        return

    if node.token.tokenType in ("VAR_DEC", "CONST_DEF"):
        # this makes sure that variables with the same name but declared within different scope
        # still have different hashed names so that they are treated as separate variables by
        # the generator and the assembly code
        if node.token.tokenType == "VAR_DEC":
            i = 1
            v = 0
        else:
            i = 0
            v = 1
        if current_scope == "global":
            id = traverse(node.operands[i])
        else:
            id = traverse(node.operands[i]) + current_scope
        # print(f'ID declared is: {id}')
        type = traverse(node.operands[v])
        line = const_var_line([id, type])
        data_definitions.append(line)

    if node.token.tokenType == "ASSIGN":
        print("test1")
        if current_scope == 'global' and node.operands[1].token.tokenType in ("NUM_LIT"):
            print("test2")
            id = ident_dic[traverse(node.operands[0])]
            for datum in data_definitions:
                if datum.udi == id:
                    print(f'test3 at datum {datum.udi}')
                    datum.value = node.operands[1].val   



    if node.token.tokenType == "MAIN":
        current_scope = "Main"
        return
        for operand in node.operands:
            traverse(operand)

        # default
    if node.operands:
        for operand in node.operands:
            traverse(operand)


def generate_code():
    global data_definitions
    global instructions
    global symbol_table
    global global_scope_content

    # start with the initialization of data definitions
    initialize_data_def()

    # by this point the data definition section has been initialized but is still not final
    traverse(root)
    print_code()

generate_code()
