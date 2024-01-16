import re
from enum import Enum 

identifier_pattern = r'[a-zA-Z_]\w*'
integer_pattern = r'\d+'
whitespace_pattern = r'\s+'
decimal_pattern = r'\d+\.\d+'
quote_pattern = r'["\'][^\n]*?["\']'
multiline_comment_pattern = r'/\*(?:.|\n)*?\*/'
inbuilt_lib_pattern = r'<[^>\n]+>' 

func_file_scope_types = ['universal', 'modular']

class Token(object):
    def __init__(self, __type__, __value__):
        self.type = __type__
        self.value = __value__

    def __repr__(self) -> str:
        return "Token({}, {})".format(self.type, self.value)
        
class TokenType(Enum):
    KEYWORD = 'KEYWORD'          # 0
    VARIABLE = 'VARIABLE'         # 1
    OPERATOR = 'OPERATOR'         # 2
    INTEGER = 'INTEGER'        # 3
    IDENTIFIER = 'IDENTIFIER'       # 4
    ENDLINE = 'ENDLINE'          # 5
    COMMENT = 'COMMENT'          # 6
    PREMACRO = 'PREMACRO'         # 7
    ADDRESS = 'ADDRESS'         # 8
    FLOAT = 'FLOAT'           # 9
    STRING = 'STRING'          # 11
    TYPE = 'TYPE'           # 12
    BINARY_VAL = 'BINARY_VAL'       # 13
    NEWLINE = 'NEWLINE'           # 14
    ASM_CALL = 'ASSEMBLY_CALL'
    EOF = 'EOF'
    FLAG = 'FLAG'
    VOID = 'VOID'
    ENDPROGRAM = "ENDPROGRAM"
    
class Operator(Enum):
    T_PLUS = '+'            # 0
    T_MINUS = '-'           # 1
    T_MULTIPLY = '*'        # 2
    T_CONS = '%'            # 3
    T_DIVIDE = '/'          # 4
    T_ENDLINE = ';'         # 5
    T_COLON = ':'           # 6
    T_LESS = '<'            # 7
    T_GREATER = '>'         # 8
    T_DOT = '.'             # 9
    T_OR = '|'              # 10
    T_EQUALS = '='          # 11
    T_LBRACE  = '('         # 12
    T_RBRACE = ')'          # 13
    T_LCBRACE = '{'         # 14
    T_RCBRACE = '}'         # 15
    T_TIDE = '~'            # 16
    T_COMA = ','            # 17
    T_ADDR = '@'            # 18
    T_EXCL = '!'            # 19
    T_LSQUAREBRACE = '['    # 20
    T_RSQUAREBRACE = ']'    # 21

class Keyword(Enum):
    ALLOC = "alloc"
    ASSIM = "assiml"
    SUBRT = "subr"
    UNIVERSAL = "universal"
    MODULAR = "modular"
    RETURN = "return"
    

class Type(Enum):
    CHT = "char"
    STR = "string"
    INT = "integer"
    FLT = "double"
    VOID = "void"
    
    
class VariableConfig:
    def __init__(self, name, value, stype):
        self.name = name
        self.value = value
        self.stype = stype
        
    def __repr__(self) -> str:
        return "Variable Name: {}\nVariable Value: {}\nVariable Stype:{}\n".format(self.name, self.value, self.stype)

class NodeType(Enum):
    FUNCTION = "Function"
    BINARY_EXPRESSION = "Binary Expression"
    FUNCTION_CALL = "Function Call"
    VARIABLE_DECL = "Variable Declaration"
    VARIABLE_REDF = "Variable Redefinition"
    LITERAL       = "Literal"
    INCLUDED_LIB  = "Included Library"
    ASSEMBLY_CALL = "Assembly Call"
    RETURN = "Return"
    
class LogicalOperators(Enum):
    FLAG = '**'
    INCREMENT = '++'
    DECREMENT = '--'
    ARROW = '->'
    
    
class LibType(Enum):
    INBUILT = "inbuilt_lib"
    USERDEFINED = "user_defined_lib"
    
class Library:
    def __init__(self, libname, libdata, libincl) -> None:
        self.libname = libname
        self.libdata = libdata
        self.global_functions = []
        self.inclfiles = libincl

        for node in self.libdata.root.children:
            if node.type == NodeType.FUNCTION:
                self.global_functions.append(node.name)
        
        
    
def T_type_conversion(type_:TokenType):
    if type_ == TokenType.INTEGER: return Type.INT
    elif type_ == TokenType.FLOAT: return Type.FLT
    elif type_ == TokenType.STRING: return Type.STR
    elif type_ == TokenType.IDENTIFIER: return TokenType.IDENTIFIER
    elif type_ == TokenType.VOID: return Type.VOID

packable_types = [NodeType.FUNCTION_CALL, NodeType.VARIABLE_DECL]

keywords        = [_.value for _ in (Keyword)]
misc_tokens     = ["/*", "*/"]
logical_ops     = [_.value for _ in (LogicalOperators)]
operators       = [_.value for _ in (Operator)]
types           = [_.value for _ in (Type)]
premacros       = ["pcbi_constant"]


string_token_t = ['"']


token_patterns = '|'.join([re.escape(keyword) for keyword in keywords] +  
                          [re.escape(misc_token) for misc_token in misc_tokens] +
                          [re.escape(logicalop) for logicalop in logical_ops] +
                          [re.escape(operator) for operator in operators] +
                          [re.escape(premacro) for premacro in premacros] + 
                          [re.escape(type_lvm) for type_lvm in types] +
                          [inbuilt_lib_pattern, identifier_pattern, whitespace_pattern, decimal_pattern, integer_pattern, quote_pattern]) 