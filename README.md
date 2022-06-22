# Green-World-Language
CSC3315 Languages & Compilers course Term Project. 
Specifications for a C-like language named Green World Language (GWL) along with End-to-End compiler with separate programs for each major step in the compilation process.

## Language Specifications
Green World Language is a C-like language in it's structure, with code blocks delimited by brackets {}, static typing, and variable declaration. To keep the project reasonable, several language features had to be simplified. Here are some notable limitations of the language:
* Only local scoping for functions. No support for nested scopes.
* Functions have to be defined in the definition section at the beggining of a program before the main function. Same for constants and global variables.
* No support for type checking.
* Some mandatory keywords were added to simplify parsing; e.g., "Call" and "Takes" are 2 keywords used to call a function as follows "Call function Takes (args)".
* GWL programs are compiled into Green World Assembly Language (GWAL), which in turn needs an interpreter of its own.

GWL is a language designed to simulate a 3-D world with a eucledian coordinate system. More details about the specifics of the language in "./Project-Part1.docx".

## Compiler Components
The compiler follows the following compilation pipeline:

![Picture1](https://user-images.githubusercontent.com/79266754/175024801-91ffd24e-8276-46be-a805-7ff254069fc2.png)

The components included in this program are as follows:
* Lexer => Tokenization | Lexical Analysis
* Parser => Syntax validation and construction of a Concrete Syntax Tree (CST)| Syntactic Analysis
* Semantic Analyzer => Defining scopes, variable declations, type assignment, arguments validation, and construction of an Abstract Syntax Tree (AST) | Semantic Analysis
* Code Generator => Generating GWAL instructions from the AST. | Code Generation

## How to Run
Each component of the compiler is a separate program importing each other in chain. 
1. The Code Generator imports and exectues the Semantic Analyzer.
2. The Semantic Analyzer imports and exectues the Parser.
3. The Parser imports and exectues the Lexer.

Each one of these programs can be executed through the command line and will prompt all the programs before it to be executed as well. Easiest way is to run "./generator.py" from the "./Generator" directory.

The program will then prompt you in the command line to enter the name of a source code file to be compiled. The source code will be fetched from the "./SampleCodes" directory. The outputs of all components will then be written onto files in the "./OutputFiles" directory.

The language lexical specifications are stored in the "./InputFiles" directory.

# Example Run

Let's try running the compiler on "./SampleCodes/source_code1.txt". Note that the purpose of the code isn't nearly as important as it being compilable.
A code with a syntax error will crash the compiler and make it log the error.

The source code is as follows 

```
qEarth :: 3;
qPlant :: 4;
Def Integer powInteger(Integer base, Integer exp){
	Dec Integer count;
	count :: 0;
	Dec Integer result;
	result :: 1;
	While(count < exp){
	result :: result * base;
	count :: count + 1;
	}
	Return result;
}
Def Fraction powFraction(Fraction base, Integer exp){
	Dec Integer count;
	count :: 0;
	Dec Fraction result;
	result :: :1.1;
	While(count < exp){
	result :: result * base;
	count :: count + 1;
	}
	Return result;
}
Dec Block a;

$CONST const 2

## the following code generates a staircase of cubic blocks of dimension 2 

Main(){
	Dec Integer dim;
	
	dim :: 2;
	Dec Integer cubeVolume;
	cubeVolume:: Call powInteger Takes (dim,3);
	Dec Integer count ;
	count :: 0;
	Dec Integer count2;
	While(count < 3){
		count2 :: 0;
		While(count2 <= count){
			qBlock :: cubeVolume;
			a :: Call MakeBlock Takes (dim,dim);
			Width :: dim*count;
			Depth :: 0;
			Height :: count2*dim;
			Call PlaceBlock Takes (a,Width,Depth,Height);
			count2 :: count2+1;
		}
		count :: count+1;
	}
}

```
After passing through the lexer, the tokens are written in "./OutputFiles/token_stream.txt" as follows:

```
1 6 QNT qEarth
1 20 ASSIGN
1 28 NUM_LIT 3
1 18 END
2 6 QNT qPlant
2 20 ASSIGN
2 28 NUM_LIT 4
2 18 END
3 3 FUNC_DEF
3 9 PRIMITIVE_TYPE Integer
3 39 IDENT powInteger
3 23 LPAREN
3 9 PRIMITIVE_TYPE Integer
3 39 IDENT base
3 19 COMMA
3 9 PRIMITIVE_TYPE Integer
3 39 IDENT exp
3 24 RPAREN
3 26 LCBRACKET
4 4 VAR_DEC
4 9 PRIMITIVE_TYPE Integer
4 39 IDENT count
4 18 END
5 39 IDENT count
5 20 ASSIGN
5 28 NUM_LIT 0
5 18 END
6 4 VAR_DEC
6 9 PRIMITIVE_TYPE Integer
6 39 IDENT result
6 18 END
7 39 IDENT result
7 20 ASSIGN
7 28 NUM_LIT 1
7 18 END
8 15 LOOP
8 23 LPAREN
8 39 IDENT count
8 31 COMP_OP <
8 39 IDENT exp
8 24 RPAREN
8 26 LCBRACKET
9 39 IDENT result
9 20 ASSIGN
9 39 IDENT result
9 30 MULT_OP *
9 39 IDENT base
9 18 END
10 39 IDENT count
10 20 ASSIGN
10 39 IDENT count
10 29 ADD_OP +
10 28 NUM_LIT 1
10 18 END
11 25 RCBRACKET
12 11 RETURN
12 39 IDENT result
12 18 END
13 25 RCBRACKET
14 3 FUNC_DEF
14 9 PRIMITIVE_TYPE Fraction
14 39 IDENT powFraction
14 23 LPAREN
14 9 PRIMITIVE_TYPE Fraction
14 39 IDENT base
14 19 COMMA
14 9 PRIMITIVE_TYPE Integer
14 39 IDENT exp
14 24 RPAREN
14 26 LCBRACKET
15 4 VAR_DEC
15 9 PRIMITIVE_TYPE Integer
15 39 IDENT count
15 18 END
16 39 IDENT count
16 20 ASSIGN
16 28 NUM_LIT 0
16 18 END
17 4 VAR_DEC
17 9 PRIMITIVE_TYPE Fraction
17 39 IDENT result
17 18 END
18 39 IDENT result
18 20 ASSIGN
18 27 FRAC_LIT :1.1
18 18 END
19 15 LOOP
19 23 LPAREN
19 39 IDENT count
19 31 COMP_OP <
19 39 IDENT exp
19 24 RPAREN
19 26 LCBRACKET
20 39 IDENT result
20 20 ASSIGN
20 39 IDENT result
20 30 MULT_OP *
20 39 IDENT base
20 18 END
21 39 IDENT count
21 20 ASSIGN
21 39 IDENT count
21 29 ADD_OP +
21 28 NUM_LIT 1
21 18 END
22 25 RCBRACKET
23 11 RETURN
23 39 IDENT result
23 18 END
24 25 RCBRACKET
25 4 VAR_DEC
25 5 PRIMITIVE_STRUCT Block
25 39 IDENT a
25 18 END
27 10 CONST_DEF
27 39 IDENT const
27 28 NUM_LIT 2
31 1 MAIN
31 23 LPAREN
31 24 RPAREN
31 26 LCBRACKET
32 4 VAR_DEC
32 9 PRIMITIVE_TYPE Integer
32 39 IDENT dim
32 18 END
34 39 IDENT dim
34 20 ASSIGN
34 28 NUM_LIT 2
34 18 END
35 4 VAR_DEC
35 9 PRIMITIVE_TYPE Integer
35 39 IDENT cubeVolume
35 18 END
36 39 IDENT cubeVolume
36 20 ASSIGN
36 2 FUNC_CALL
36 39 IDENT powInteger
36 17 TAKE
36 23 LPAREN
36 39 IDENT dim
36 19 COMMA
36 28 NUM_LIT 3
36 24 RPAREN
36 18 END
37 4 VAR_DEC
37 9 PRIMITIVE_TYPE Integer
37 39 IDENT count
37 18 END
38 39 IDENT count
38 20 ASSIGN
38 28 NUM_LIT 0
38 18 END
39 4 VAR_DEC
39 9 PRIMITIVE_TYPE Integer
39 39 IDENT count2
39 18 END
40 15 LOOP
40 23 LPAREN
40 39 IDENT count
40 31 COMP_OP <
40 28 NUM_LIT 3
40 24 RPAREN
40 26 LCBRACKET
41 39 IDENT count2
41 20 ASSIGN
41 28 NUM_LIT 0
41 18 END
42 15 LOOP
42 23 LPAREN
42 39 IDENT count2
42 31 COMP_OP <=
42 39 IDENT count
42 24 RPAREN
42 26 LCBRACKET
43 6 QNT qBlock
43 20 ASSIGN
43 39 IDENT cubeVolume
43 18 END
44 39 IDENT a
44 20 ASSIGN
44 2 FUNC_CALL
44 8 PRIMITIVE_FUNC MakeBlock
44 17 TAKE
44 23 LPAREN
44 39 IDENT dim
44 19 COMMA
44 39 IDENT dim
44 24 RPAREN
44 18 END
45 7 PRIMITIVE_DIM Width
45 20 ASSIGN
45 39 IDENT dim
45 30 MULT_OP *
45 39 IDENT count
45 18 END
46 7 PRIMITIVE_DIM Depth
46 20 ASSIGN
46 28 NUM_LIT 0
46 18 END
47 7 PRIMITIVE_DIM Height
47 20 ASSIGN
47 39 IDENT count2
47 30 MULT_OP *
47 39 IDENT dim
47 18 END
48 2 FUNC_CALL
48 8 PRIMITIVE_FUNC PlaceBlock
48 17 TAKE
48 23 LPAREN
48 39 IDENT a
48 19 COMMA
48 7 PRIMITIVE_DIM Width
48 19 COMMA
48 7 PRIMITIVE_DIM Depth
48 19 COMMA
48 7 PRIMITIVE_DIM Height
48 24 RPAREN
48 18 END
49 39 IDENT count2
49 20 ASSIGN
49 39 IDENT count2
49 29 ADD_OP +
49 28 NUM_LIT 1
49 18 END
50 25 RCBRACKET
51 39 IDENT count
51 20 ASSIGN
51 39 IDENT count
51 29 ADD_OP +
51 28 NUM_LIT 1
51 18 END
52 25 RCBRACKET
53 25 RCBRACKET

```

The token stream is then fed to the parser which is following the grammar syntax of the language and outputs the following CST:

"./OutputFiles/CST.txt"
```
LAN --- PRG --- ASG --- qEarth
                    --- ::
                    --- <E> --- <T> --- <F> --- <V> --- 3
            --- ;
            --- ASG --- qPlant
                    --- ::
                    --- <E> --- <T> --- <F> --- <V> --- 4
            --- ;
            --- FND --- Def
                    --- TYP --- Integer
                    --- powInteger
                    --- (
                    --- PAR --- TYP --- Integer
                            --- base
                            --- ,
                            --- TYP --- Integer
                            --- exp
                    --- )
                    --- {
                    --- TCB --- STM --- DEC --- Dec
                                            --- TYP --- Integer
                                            --- count
                                    --- ;
                            --- STM --- ASG --- count
                                            --- ::
                                            --- <E> --- <T> --- <F> --- <V> --- 0
                                    --- ;
                            --- STM --- DEC --- Dec
                                            --- TYP --- Integer
                                            --- result
                                    --- ;
                            --- STM --- ASG --- result
                                            --- ::
                                            --- <E> --- <T> --- <F> --- <V> --- 1
                                    --- ;
                            --- STM --- JMP --- LOP --- loop
                                                    --- (
                                                    --- BLE --- BLT --- BLF --- CMP --- <E> --- <T> --- <F> --- <V> --- count
                                                                                    --- <
                                                                                    --- CMP --- <E> --- <T> --- <F> --- <V> --- exp
                                                    --- )
                                                    --- {
                                                    --- TCB --- STM --- ASG --- result
                                                                            --- ::
                                                                            --- <E> --- <T> --- <F> --- <V> --- result
                                                                                            --- *
                                                                                            --- <T> --- <F> --- <V> --- base
                                                                    --- ;
                                                            --- STM --- ASG --- count
                                                                            --- ::
                                                                            --- <E> --- <T> --- <F> --- <V> --- count
                                                                                    --- +
                                                                                    --- <E> --- <T> --- <F> --- <V> --- 1
                                                                    --- ;
                                                    --- }
                            --- STM --- JMP --- return
                                            --- <E> --- <T> --- <F> --- <V> --- result
                                    --- ;
                    --- }
            --- FND --- Def
                    --- TYP --- Fraction
                    --- powFraction
                    --- (
                    --- PAR --- TYP --- Fraction
                            --- base
                            --- ,
                            --- TYP --- Integer
                            --- exp
                    --- )
                    --- {
                    --- TCB --- STM --- DEC --- Dec
                                            --- TYP --- Integer
                                            --- count
                                    --- ;
                            --- STM --- ASG --- count
                                            --- ::
                                            --- <E> --- <T> --- <F> --- <V> --- 0
                                    --- ;
                            --- STM --- DEC --- Dec
                                            --- TYP --- Fraction
                                            --- result
                                    --- ;
                            --- STM --- ASG --- result
                                            --- ::
                                            --- <E> --- <T> --- <F> --- <V> --- :1.1
                                    --- ;
                            --- STM --- JMP --- LOP --- loop
                                                    --- (
                                                    --- BLE --- BLT --- BLF --- CMP --- <E> --- <T> --- <F> --- <V> --- count
                                                                                    --- <
                                                                                    --- CMP --- <E> --- <T> --- <F> --- <V> --- exp
                                                    --- )
                                                    --- {
                                                    --- TCB --- STM --- ASG --- result
                                                                            --- ::
                                                                            --- <E> --- <T> --- <F> --- <V> --- result
                                                                                            --- *
                                                                                            --- <T> --- <F> --- <V> --- base
                                                                    --- ;
                                                            --- STM --- ASG --- count
                                                                            --- ::
                                                                            --- <E> --- <T> --- <F> --- <V> --- count
                                                                                    --- +
                                                                                    --- <E> --- <T> --- <F> --- <V> --- 1
                                                                    --- ;
                                                    --- }
                            --- STM --- JMP --- return
                                            --- <E> --- <T> --- <F> --- <V> --- result
                                    --- ;
                    --- }
            --- DEC --- Dec
                    --- TYP --- Block
                    --- a
            --- ;
            --- CST --- $CONST
                    --- const
                    --- <E> --- <T> --- <F> --- <V> --- 2
            --- MNF --- Main
                    --- (
                    --- )
                    --- {
                    --- TCB --- STM --- DEC --- Dec
                                            --- TYP --- Integer
                                            --- dim
                                    --- ;
                            --- STM --- ASG --- dim
                                            --- ::
                                            --- <E> --- <T> --- <F> --- <V> --- 2
                                    --- ;
                            --- STM --- DEC --- Dec
                                            --- TYP --- Integer
                                            --- cubeVolume
                                    --- ;
                            --- STM --- ASG --- cubeVolume
                                            --- ::
                                            --- <E> --- <T> --- <F> --- <V> --- FNC --- call
                                                                                    --- powInteger
                                                                                    --- take
                                                                                    --- (
                                                                                    --- ARG --- <E> --- <T> --- <F> --- <V> --- dim
                                                                                            --- ,
                                                                                            --- <E> --- <T> --- <F> --- <V> --- 3
                                                                                    --- )
                                    --- ;
                            --- STM --- DEC --- Dec
                                            --- TYP --- Integer
                                            --- count
                                    --- ;
                            --- STM --- ASG --- count
                                            --- ::
                                            --- <E> --- <T> --- <F> --- <V> --- 0
                                    --- ;
                            --- STM --- DEC --- Dec
                                            --- TYP --- Integer
                                            --- count2
                                    --- ;
                            --- STM --- JMP --- LOP --- loop
                                                    --- (
                                                    --- BLE --- BLT --- BLF --- CMP --- <E> --- <T> --- <F> --- <V> --- count
                                                                                    --- <
                                                                                    --- CMP --- <E> --- <T> --- <F> --- <V> --- 3
                                                    --- )
                                                    --- {
                                                    --- TCB --- STM --- ASG --- count2
                                                                            --- ::
                                                                            --- <E> --- <T> --- <F> --- <V> --- 0
                                                                    --- ;
                                                            --- STM --- JMP --- LOP --- loop
                                                                                    --- (
                                                                                    --- BLE --- BLT --- BLF --- CMP --- <E> --- <T> --- <F> --- <V> --- count2
                                                                                                                    --- <=
                                                                                                                    --- CMP --- <E> --- <T> --- <F> --- <V> --- count
                                                                                    --- )
                                                                                    --- {
                                                                                    --- TCB --- STM --- ASG --- qBlock
                                                                                                            --- ::
                                                                                                            --- <E> --- <T> --- <F> --- <V> --- cubeVolume
                                                                                                    --- ;
                                                                                            --- STM --- ASG --- a
                                                                                                            --- ::
                                                                                                            --- <E> --- <T> --- <F> --- <V> --- FNC --- call
                                                                                                                                                    --- MakeBlock
                                                                                                                                                    --- take
                                                                                                                                                    --- (
                                                                                                                                                    --- ARG --- <E> --- <T> --- <F> --- <V> --- dim
                                                                                                                                                            --- ,
                                                                                                                                                            --- <E> --- <T> --- <F> --- <V> --- dim
                                                                                                                                                    --- )
                                                                                                    --- ;
                                                                                            --- STM --- ASG --- Width
                                                                                                            --- ::
                                                                                                            --- <E> --- <T> --- <F> --- <V> --- dim
                                                                                                                            --- *
                                                                                                                            --- <T> --- <F> --- <V> --- count
                                                                                                    --- ;
                                                                                            --- STM --- ASG --- Depth
                                                                                                            --- ::
                                                                                                            --- <E> --- <T> --- <F> --- <V> --- 0
                                                                                                    --- ;
                                                                                            --- STM --- ASG --- Height
                                                                                                            --- ::
                                                                                                            --- <E> --- <T> --- <F> --- <V> --- count2
                                                                                                                            --- *
                                                                                                                            --- <T> --- <F> --- <V> --- dim
                                                                                                    --- ;
                                                                                            --- STM --- FNC --- call
                                                                                                            --- PlaceBlock
                                                                                                            --- take
                                                                                                            --- (
                                                                                                            --- ARG --- <E> --- <T> --- <F> --- <V> --- a
                                                                                                                    --- ,
                                                                                                                    --- <E> --- <T> --- <F> --- <V> --- Width
                                                                                                                    --- ,
                                                                                                                    --- <E> --- <T> --- <F> --- <V> --- Depth
                                                                                                                    --- ,
                                                                                                                    --- <E> --- <T> --- <F> --- <V> --- Height
                                                                                                            --- )
                                                                                                    --- ;
                                                                                            --- STM --- ASG --- count2
                                                                                                            --- ::
                                                                                                            --- <E> --- <T> --- <F> --- <V> --- count2
                                                                                                                    --- +
                                                                                                                    --- <E> --- <T> --- <F> --- <V> --- 1
                                                                                                    --- ;
                                                                                    --- }
                                                            --- STM --- ASG --- count
                                                                            --- ::
                                                                            --- <E> --- <T> --- <F> --- <V> --- count
                                                                                    --- +
                                                                                    --- <E> --- <T> --- <F> --- <V> --- 1
                                                                    --- ;
                                                    --- }

```

The Semantic Analyzer reduces down the CST to the following AST:

"./OutputFiles/AST.txt"
```
PRG --- :: ---- qEarth
           ---- 3
    --- :: ---- qPlant
           ---- 4
    --- Def --- Integer
            --- Integer  base
            --- Integer  exp
            --- Dec --- Integer
                    --- count
            --- :: ---- count
                   ---- 0
            --- Dec --- Integer
                    --- result
            --- :: ---- result
                   ---- 1
            --- loop -- < ----- count
                          ----- exp
                     -- :: ---- result
                           ---- * ----- result
                                  ----- base
                     -- :: ---- count
                           ---- + ----- count
                                  ----- 1
            --- return  result
    --- Def --- Fraction
            --- Fraction  base
            --- Integer  exp
            --- Dec --- Integer
                    --- count
            --- :: ---- count
                   ---- 0
            --- Dec --- Fraction
                    --- result
            --- :: ---- result
                   ---- :1.1
            --- loop -- < ----- count
                          ----- exp
                     -- :: ---- result
                           ---- * ----- result
                                  ----- base
                     -- :: ---- count
                           ---- + ----- count
                                  ----- 1
            --- return  result
    --- Dec --- Block
            --- a
    --- $CONST  const
                2
    --- Main -- Dec --- Integer
                    --- dim
             -- :: ---- dim
                   ---- 2
             -- Dec --- Integer
                    --- cubeVolume
             -- :: ---- cubeVolume
                   ---- call -- powInteger
                             -- take -- dim
                                     -- 3
             -- Dec --- Integer
                    --- count
             -- :: ---- count
                   ---- 0
             -- Dec --- Integer
                    --- count2
             -- loop -- < ----- count
                          ----- 3
                     -- :: ---- count2
                           ---- 0
                     -- loop -- <= ---- count2
                                   ---- count
                             -- :: ---- qBlock
                                   ---- cubeVolume
                             -- :: ---- a
                                   ---- call -- MakeBlock
                                             -- take -- dim
                                                     -- dim
                             -- :: ---- Width
                                   ---- * ----- dim
                                          ----- count
                             -- :: ---- Depth
                                   ---- 0
                             -- :: ---- Height
                                   ---- * ----- count2
                                          ----- dim
                             -- call -- PlaceBlock
                                     -- take -- a
                                             -- Width
                                             -- Depth
                                             -- Height
                             -- :: ---- count2
                                   ---- + ----- count2
                                          ----- 1
                     -- :: ---- count
                           ---- + ----- count
                                  ----- 1

```

The Semantic Analyzer also outputs a Symbol Table containing meta data about functions, variables, constants, scopes, etc.

"./OutputFiles/symbol_table.txt"
```
----------- Symbol Table ------------

Integer : {'category': 'type', 'scope': 'global'}
Fraction : {'category': 'type', 'scope': 'global'}
Void : {'category': 'type', 'scope': 'global'}
Block : {'category': 'type', 'scope': 'global'}
Tub : {'category': 'type', 'scope': 'global'}
Earth : {'category': 'type', 'scope': 'global'}
Plant : {'category': 'type', 'scope': 'global'}
qBlock : {'category': 'variable', 'scope': 'global'}
qTub : {'category': 'variable', 'scope': 'global'}
qEarth : {'category': 'variable', 'scope': 'global'}
qPlant : {'category': 'variable', 'scope': 'global'}
Width : {'category': 'function', 'scope': 'global', 'parameters': {}}
Depth : {'category': 'function', 'scope': 'global', 'parameters': {}}
Height : {'category': 'function', 'scope': 'global', 'parameters': {}}
MakeBlock : {'category': 'function', 'scope': 'global', 'parameters': {'width': 'Integer', 'depth': 'Integer'}}
UnmakeBlock : {'category': 'function', 'scope': 'global', 'parameters': {'block': 'Block'}}
MakeTub : {'category': 'function', 'scope': 'global', 'parameters': {'width': 'Integer', 'depth': 'Integer', 'height': 'Integer'}}
UnmakeTub : {'category': 'function', 'scope': 'global', 'parameters': {'tub': 'Tub'}}
PlaceBlock : {'category': 'function', 'scope': 'global', 'parameters': {'block': 'Block', 'x': 'Integer', 'y': 'Integer', 'z': 'Integer'}}
PlaceTub : {'category': 'function', 'scope': 'global', 'parameters': {'tub': 'Tub', 'x': 'Integer', 'y': 'Integer', 'z': 'Integer'}}
MakePlant : {'category': 'function', 'scope': 'global', 'parameters': {'size': 'Integer'}}
UnmakePlant : {'category': 'function', 'scope': 'global', 'parameters': {'plant': 'Plant'}}
AddEarth : {'category': 'function', 'scope': 'global', 'parameters': {'tub': 'Tub', 'quantity': 'Fraction'}}
RemoveEarth : {'category': 'function', 'scope': 'global', 'parameters': {'tub': 'Tub', 'quantity': 'Fraction'}}
Sow : {'category': 'function', 'scope': 'global', 'parameters': {'tub': 'Tub', 'plant': 'Plant'}}
Uproot : {'category': 'function', 'scope': 'global', 'parameters': {'tub': 'Tub'}}
$CONST : {'category': 'statement', 'scope': 'global'}
Return : {'category': 'statement', 'scope': 'global'}
If : {'category': 'statement', 'scope': 'global'}
Then : {'category': 'statement', 'scope': 'global'}
Else : {'category': 'statement', 'scope': 'global'}
While : {'category': 'statement', 'scope': 'global'}
Takes : {'category': 'statement', 'scope': 'global'}
Dec : {'category': 'statement', 'scope': 'global'}
Def : {'category': 'statement', 'scope': 'global'}
Call : {'category': 'statement', 'scope': 'global'}
powInteger : {'category': 'function', 'scope': 'global', 'parameters': {'base': 'Integer', 'exp': 'Integer'}}
base : {'category': 'variable', 'scope': 'local'}
exp : {'category': 'variable', 'scope': 'local'}
count : {'category': 'variable', 'scope': 'local'}
result : {'category': 'variable', 'scope': 'local'}
powFraction : {'category': 'function', 'scope': 'global', 'parameters': {'base': 'Fraction', 'exp': 'Integer'}}
a : {'category': 'variable', 'scope': 'global'}
const : {'category': 'constant', 'scope': 'global'}
dim : {'category': 'variable', 'scope': 'local'}
cubeVolume : {'category': 'variable', 'scope': 'local'}
count2 : {'category': 'variable', 'scope': 'local'}
-------------------------------------
```

Lastly, the code generators uses all of that to generate GWAL instructions (see GWAL specifications). Note that the Generator is currently incomplete and only generates GWAL code for the definitions section.

"./OutputFiles/assembly.txt"
```
PROGRAM	generated
## This comment is just here to test comments
DATA

## This is where you would place DataDefinitions
VAR	WORLD	INT	4000	0
VAR	OTMLOG	INT	1	30
VAR	OTGYTH	INT	1	22
VAR	RMHXXA	INT	1	3
VAR	BNZVOW	INT	1	4
VAR	TEMP1	INT		
VAR	TEMP2	INT		
VAR	TEMP3	INT		
VAR	TEMP4	INT		
CONST	TEXT	STRING	0	*
This is supposed to be a constant long string
VAR	QWOXCQ	INT	1	
VAR	IADRZV	Integer		0
VAR	CSVBFS	Integer		1
VAR	IADRZV	Integer		0
VAR	CSVBFS	Fraction		
VAR	EWSUBM	Block		
CONST	KEGDFC	2		

CODE
## This is where Executable Instructions go

```


