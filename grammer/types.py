from manifest.tokens import *

def convert_obj_to_tokens(PyObject):
    if type(PyObject) == str:
        return Token(TokenType.STRING, PyObject)
    
    elif type(PyObject) == int:
        return Token(TokenType.INTEGER, PyObject)
    
    elif type(PyObject) == float:
        return Token(TokenType.FLOAT, PyObject)