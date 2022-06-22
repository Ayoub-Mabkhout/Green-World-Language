import sys
import re
import csv
sys.path.append('../')
path = sys.path.pop()
input_folder = path+"InputFiles/"
code_folder = path+"SampleCodes/"
out_folder = path+"OutputFiles/"
lastToken = "NOTHING"
n_token = 0
whiteSpaces = [' ', '\t', '\n']
symbol_table = {}
tokens = []


# loads source code file


def loadFile(filepath):
    with open(filepath) as f:
        return f.read()


# def readCode():
#     pos = Position()
#     for letter in code:
#         pos.advance(letter)
#         print(pos.lastchar + " in line: " +
#               str(pos.ln) + " and column: " + str(pos.col))

# Position class containing the position information for every character/token
# Used in the Lexer for assigning a line attribute to each token
# May be used for debugging purposes


class Position:
    def __init__(self):
        self.ln = 1
        self.col = 0
        self.lastchar = ''

# Position ignores tabulations and empty spaces, but not new lines
    def advance(self, currentChar):
        if(currentChar == '\t' or currentChar == ' '):
            return

        self.col += 1
        self.lastchar = currentChar

        if(currentChar == '\n'):
            self.col = 0
            self.ln += 1

# each token as a token type, and the token type has 4 attributes
# those are the type itself (e.g., IDENT), the regular expression
# a boolean flag to determine if the token takes in a value/attribute
# and a tokenID associated with the token type


class TokenType:
    def __init__(self, type, regex, val_flag, ID):
        self.tokenType = type
        self.val_flag = val_flag
        self.regex = regex
        self.tokenID = ID

    # __repr__() method was used for debugging
    def __repr__(self):
        return "TYPE: " + self.tokenType + " REGEX: " + self.regex + " VALUE? " + str(self.val_flag)


# the tokenTypes list is initialized by loading the token types from a .csv file
# with each field/column in that .csv file representing one of the attributes of TokenType
tokenTypes = []


def loadTokenTypes():
    file = open(input_folder + 'tokens.csv')
    reader = csv.reader(file)
    for line in reader:
        newType = TokenType(line[1], line[0] if line[0]
                            != 'comma' else ',', line[2], line[3])
        tokenTypes.append(newType)

    # print loop for debugging (commented out)

    # idx = 0
    # for type in tokenTypes:
    #         print(f'{idx}. {type}')
    #         idx += 1
    # print("\n")

# if the certain reserved word is a function, we might want to use this method to parse its parameters and add them to the symbol table


def parse_parameters(line):
    try:
        line = line.strip()
        par = {}
        if not line:
            return par
        parameters = line.split("|")
        for elt in parameters:
            type = elt.split(":")[0]
            name = elt.split(":")[1]
            par[name] = type
        return par
    except IndexError as e:
        raise IndexOutOfRangeError(elt, 1)


# initializing symbol table with reserved words and their default key-value pairs
# the information for reserved words comes in a .csv file, namely the name of the symbol, the category (variable or function or else),
# and possibly the parameters for the functions
def initialize_st():
    global symbol_table
    f = open(input_folder + 'reserved_words.csv')
    reader = csv.reader(f)
    for record in reader:
        symbol_table[record[0]] = {"category": record[1], "scope": "global"}
        if record[1] == "function":
            par = parse_parameters(record[2])
            symbol_table[record[0]]["parameters"] = par


# each instance of the class Token is an actual token that has been parsed from the input code
# and that is added to the lexer's token stream output
class Token:
    def __init__(self, type, value, line):
        self.line = line
        self.tokenValue = value
        self.idx = 0
        for t_type in tokenTypes:
            if(t_type.tokenType == type):
                break
            self.idx += 1
        else:
            self.idx = -1
            # raise Invalid Token Exception
        self.tokenType = type
        # print statement below for debugging
        # print(f'SELF.IDX IS EQUAL TO {self.idx} AND TOKENTYPE IS {self.tokenType}')

        if self.idx == -1:
            self.tokenID = None
        else:
            self.tokenID = tokenTypes[self.idx].tokenID

    # __repr__() method is called when writing tokens into the token stream output
    # it gives an output that is identical to that of the example shown in the instruction documnent
    def __repr__(self):
        t = str(self.line) + " " + str(self.tokenID) + " " + self.tokenType
        if(self.idx != -1):
            if(tokenTypes[self.idx].val_flag != "FALSE"):
                t = t + " " + str(self.tokenValue)
        else:
            t = t + " " + str(self.tokenValue)
        return t


class InvalidTokenError(Exception):
    def __init__(self, token_value, line):
        self.message = f'Invalid Token: {token_value} at line {line}'
        self.token_value = token_value
        self.line = line
        super().__init__(self.message)


class IndexOutOfRangeError(Exception):
    def __init__(self, list, index):
        self.message = f'Index out of range error with list {list} and index {index}'
        super().__init__(self.message)


# the Lexer class is the most important class in here
# it makes use of all the classes and most of the methods defined above
# and is charged of converting an input code into a file containing a token stream

class Lexer:

    # the an object of the Lexer class is instanciated, it takes an input code as an argument
    # other input files will be needed as well, namely a "tokens.csv" to import the token types
    # for the language and a "reserver_words.txt" file to import the reserved words for the symbol table
    def __init__(self, code):
        print("\n\n")
        print("--------------------------------------")
        print("--------- Initializing Lexer ---------")
        print("--------------------------------------")
        print("\n\n")
        self.code = code
        self.pos = -1
        self.previousChar = None
        self.currentChar = None
        self.debug_pos = Position()
        try:
            loadTokenTypes()
            self.advance()
            self.makeTokens()
            print(symbol_table.keys())
        except InvalidTokenError as e:
            print(f'Error: {e.message}')
            exit()
        except IndexOutOfRangeError as e:
            print(f'Error: {e.message}')
            exit()

    # the lexer reads the code letter by letter

    def advance(self):
        self.pos += 1
        self.previousChar = self.currentChar
        self.currentChar = self.code[self.pos] if self.pos < len(
            self.code) else None

    # checks if a string that is given as an argument matches with the regular expression for
    # one of the token types imported in the .csv file
    # returns the first token type with which there is a match
    # else returns none
    def matchToken(self, buildingToken):
        for i in range(len(tokenTypes)):
            types = tokenTypes[i]
            # print(str(i) +". matching " + buildingToken + " with " + types.regex)
            if re.fullmatch(types.regex, buildingToken):
                # print("MATCH!!")
                return types.tokenType
        return None

    # this method is charged of writing the output both into the tokens file and the terminal
    def printTokens(self, tokens, symbols):
        global symbol_table
        with open(out_folder+"token_stream.txt", "w+") as f:
            for token in tokens:
                f.write(f'{token}\n')
                t_value = token.tokenValue
                if t_value == " ":
                    t_value = "[SPACE]"
                elif t_value == "\t":
                    t_value = "\\t"
                elif t_value == "\n":
                    t_value = "\\n"
                print(f'Line {token.line} Token #{token.tokenID}: {t_value}')

        for symbol in symbols:
            symbol_table[symbol] = {"category": None, "scope": None}

    # small method to do everything associated with adding a token once a token has been parsed

    def append_token(self, token, tokens, symbols):
        tokens.append(token)
        if token.tokenType == "IDENT" and token.tokenValue not in symbols:
            symbols.append(token.tokenValue)

    # this method contains the algorithm for parsing tokens from the source code file
    # it ignores white spaces, makes sure individual tokens cannot contain white spaces,
    # and determines whether a token is valid or not
    # this approach made the implementation of comments quite problematic
    def makeTokens(self):
        inline_cmnt = False
        mlt_line_cmnt = False
        buildingToken = ""
        global tokens
        symbols = []
        initialize_st()
        i = 0

        while self.currentChar != None:
            append_flag = False
            append_token = ""
            i += 1
            if self.currentChar in whiteSpaces:
                if self.previousChar in whiteSpaces:
                    if self.currentChar == "\n":
                        inline_cmnt = False
                else:
                    b_token = buildingToken[0: len(buildingToken)]
                    x = self.matchToken(b_token)
                    if not x and not (inline_cmnt or mlt_line_cmnt):
                        # self.append_token(Token("INVALID TOKEN", b_token, self.debug_pos.ln),tokens,symbols)
                        raise InvalidTokenError(
                            b_token, self.debug_pos.ln)
                        buildingToken = ""
                    elif x == "SNG_LN_CMNT":
                        inline_cmnt = True
                    # elif self.currentChar == "\n":
                    #     inline_cmnt = False
                    elif x == "BEG_CMNT":
                        mlt_line_cmnt = True
                    elif x == "END_CMNT":
                        mlt_line_cmnt = False
                    else:
                        # self.append_token(Token(x, b_token, self.debug_pos.ln),tokens,symbols)
                        append_flag = True
                        append_token = (x, b_token)

                    buildingToken = ""
                # if self.currentChar == "\n":
                #     inline_cmnt = False

            else:
                buildingToken += self.currentChar
                x = self.matchToken(buildingToken)
                y = self.matchToken(buildingToken[0: len(buildingToken)-1])

                if x == "SNG_LN_CMNT":
                    inline_cmnt = True
                # elif self.currentChar == "\n":
                #     inline_cmnt = False
                elif x == "BEG_CMNT":
                    mlt_line_cmnt = True
                elif x == "END_CMNT":
                    mlt_line_cmnt = False
                elif y and not x:
                    b_token = buildingToken[0: len(buildingToken)-1]
                    # self.append_token(Token(y, b_token, self.debug_pos.ln),tokens,symbols)
                    append_flag = True
                    append_token = (y, b_token)
                    buildingToken = buildingToken[len(buildingToken)-1]

            if(append_flag and not(inline_cmnt or mlt_line_cmnt)):
                if append_token[0] != "END_CMNT":
                    self.append_token(
                        Token(append_token[0], append_token[1], self.debug_pos.ln), tokens, symbols)
            # code has to end with some form of whiteSpace for the last token to be counted
            self.debug_pos.advance(self.currentChar)
            self.advance()

        self.printTokens(tokens, symbols)

filename = code_folder + input("Enter source code file name:\t")
code = loadFile(filename)
# code = loadFile(filename)
# # readCode()
lexer = Lexer(code)
