# Copyright (c) Aarav Shreshth, 2025
# 
# Author    - Aarav Shreshth
# File Name - parser_buzz.py
#

import os
import inspect

from manifest import *
from manifest.astz   import *
from manifest.tokens import *
from grammer.errors import Error
from grammer.types import convert_obj_to_tokens
from buzz import *

# Main parser class

class ZParser(object):
    def __init__(self, tokens_, filename):
        self.hasmain = False
        self.islib = filename.endswith('bl')    
        self.filename = filename
        self.tokens_ = tokens_
        self.ast = Ast()
        self.index = 0
        self.infun = False
        
        # Program Libraries
        self.included_libraries = []
        
    def Parse(self):        
        self.index = 0
        while self.index<len(self.tokens_):
            tokentype = self.tokens_[self.index].type
            tokenvalue = self.tokens_[self.index].value
            if tokentype == TokenType.KEYWORD:
                
                if tokenvalue in func_file_scope_types and self.tokens_[self.index+1].value == 'subr' or tokenvalue == 'subr':
                    
                    if tokenvalue != 'subr':
                        func, a= self.ParseFunctions( self.tokens_[self.index+1:len(self.tokens_)], tokenvalue)
                        self.ast.add_node(self.ast.root, func) 
                        self.index+=a
                        
                        
                        
                    else:
                        func, a= self.ParseFunctions(self.tokens_[self.index:len(self.tokens_)], 'modular')
                        self.ast.add_node(self.ast.root, func) 
                        self.index+=a
               
                        
            # elif tokentype == TokenType.FLAG:
            #     if tokenvalue == "module":
            #         self.ParseModuleFlag(self.tokens_[self.index:])
                    
            if tokentype == TokenType.TYPE:
                if self.GetNextToken().type == TokenType.IDENTIFIER:
                    # print('yes')
                    vardecl, i = self.ParseVariableDecl(self.tokens_[self.index:len(self.tokens_)])
                    self.ast.add_node(self.ast.root, vardecl)
                    self.index+=i

                        
            if tokentype == TokenType.IDENTIFIER:
                # print(self.infun)
                # print(self.tokens_[self.index])
                
                if self.tokens_[self.index+1].type == TokenType.OPERATOR and self.tokens_[self.index+1].value == "(" and self.tokens_[self.index-1].value != "subr":
                    fcll = self.ParseFunctionCall(self.tokens_[self.index:len(self.tokens_)])
                    self.ast.add_node(self.ast.root, fcll)
                    # self.index+=1

                
            self.index+=1

        return self.ast, self.included_libraries
    
    def parse_and_increment(self, parse_method, tokens, kwargs:...):
        node = parse_method(tokens, kwargs)
        
        self.index += len(tokens)
        return node
    
    def GetNextToken(self):
        if self.index<len(self.tokens_):
            return self.tokens_[self.index+1]
        else:
            return None
    
    def ParseVariableDecl(self, token_stream):
        # print(token_stream)
        i = 0
        varname = None
        vartype = None
        varvalue = []

        type_ = token_stream[i].type
        value = token_stream[i].value
        vartype = value
        
        i+=1
        type_ = token_stream[i].type
        value = token_stream[i].value

        if type_ == TokenType.IDENTIFIER: 
            varname = value 
            i+=1

        else:
            print("E: Expected variable name for variable declaration.")
            exit(1)

        type_ = token_stream[i].type
        value = token_stream[i].value

        if type_ != TokenType.OPERATOR or type_ == TokenType.OPERATOR and value != '=':
            print(f"E: Expected '=' op for value assignment, got {value}")
            exit(1)

        i+=1

        type_ = token_stream[i].type
        value = token_stream[i].value

        while value != ';':
            type_ = token_stream[i].type
            value = token_stream[i].value 

            varvalue.append(Token(type_, value))

            if varvalue[-1].value == ';':
                varvalue.pop(-1)
              
            i+=1
            
        # if len(varvalue) ==1:
        #     varvalue = varvalue[0]
            
        nd = VariableDeclNode(varname, NodeType.VARIABLE_DECL, varvalue, vartype)
        # print(nd)
        return nd, i
        
    def ParseModuleFlag(self, tokens_):
        tokens = tokens_
        i = 0
        modulepath = None
        module_startline = None
        module_endline = None
        modulebody = []
        
        in_st = True
        
        type_ = tokens[i].type
        value = tokens[i].value
        i+=1
        
        if type_ == TokenType.STRING:
            modulepath = value
            i+=1
            
        type_ = tokens[i].type
        value = tokens[i].value
        
        if type_ == TokenType.INTEGER:
            module_startline = value
            i+=1
            
        type_ = tokens[i].type
        value = tokens[i].value
        i+=1
        if type_ == TokenType.ENDLINE:
            in_st = False
        i+=1
            
        in_bd = True
        type_ = tokens[i].type
        value = tokens[i].value
        i+=1
        
        while in_bd:
            type_ = tokens[i].type
            value = tokens[i].value
            
            modulebody.append(Token(type_, value))
            
            if tokens[i+1].value == 'endmodule': in_bd = False
            
            i+=1

        
            
            
    def ParseLiteral(self, tokens_) -> Node:
        tokens = tokens_
        for tok in tokens_:
            # print(tok.type)
            if tok.type in [TokenType.STRING, TokenType.INTEGER, TokenType.FLOAT, TokenType.IDENTIFIER]:
                return Node('Literal', NodeType.LITERAL, tok.value, T_type_conversion(tok.type))

 
    def ParseFunctions(self, tok, scope):
        i = 0
        funcname = None
        funcargs = []
        funcretype = None
        funcbody = []
        func_file_scope_type = scope
        
        self.infun = True
        type_ = tok[i].type
        value = tok[i].value


        if type_ == TokenType.KEYWORD and value == "subr":
            i+=1
            type_ = tok[i].type
            value = tok[i].value
            
        type_ = tok[i].type
        value = tok[i].value
            
        
        if type_ == TokenType.IDENTIFIER:
            funcname = value
            i+=1

        type_ = tok[i].type
        value = tok[i].value
        
        if type_ ==TokenType.OPERATOR and value == '(':
            pass
        
        else: Error(self.filename, 'error', f"expected '(' to declare parameters.", 1, True)

        i+=1
        
        type_ = tok[i].type
        value = tok[i].value
        
        if type_==TokenType.OPERATOR and value == ')':
            in_arg = False
            
        in_arg = True
        while in_arg:
            type_ = tok[i].type
            value = tok[i].value
            funcargs.append(Token(type_, value))
            # if tok[i].type == TokenType.OPERATOR and tok[i].value == '~': 
            #     funcargs.append({Token(tok[i-1].type, tok[i-1].value): Token(tok[i+1].type, tok[i+1].value)})
            if tok[i].type == TokenType.OPERATOR and tok[i].value == ')': in_arg = False
            
            i+=1

        if len(funcargs) != 0:
            if funcargs[-1].type == TokenType.OPERATOR and funcargs[-1].value == ')':
                funcargs.pop(-1)
                
        
        _Sd = 0
        
        
        real_arg = {}
        final_args = []
        
        _name = None
        _type = None
        
        while _Sd < len(funcargs):
            
            toki = funcargs[_Sd]
            if toki.type == TokenType.IDENTIFIER:
                _name = toki.value
                
                if funcargs[_Sd+1].type == TokenType.OPERATOR and funcargs[_Sd+1].value == "~":
                    if funcargs[_Sd+2].type == TokenType.TYPE:
                        _type = funcargs[_Sd+2].value
                        
                        real_arg[_name] = _type
                        
                        _Sd+=3
                        
            
            _tmp = ArgumentNode(_name, _type)
            final_args.append(_tmp)   
            
            _Sd+=1
            
            
        type_ = tok[i].type
        value = tok[i].value
        
        if type_ == TokenType.ADDRESS:
            i+=1
                        
            type_ = tok[i].type
            value = tok[i].value
            # print(type_)
            if value in [Type.INT.value, Type.FLT.value, Type.STR.value, Type.VOID.value]:
                # print('2')
                funcretype = value
                
            i+=1
            
        else: Error(self.filename, 'error', f"expected '@' to define function type.", 1, True)
            
        type_ = tok[i].type
        value = tok[i].value
        
        
        if type_==TokenType.OPERATOR and value == "{":
            i+=1
            in_body = True
            # print(type_, value, "hello")
            
            type_ = tok[i].type
            value = tok[i].value
            
            while in_body:
                type_ = tok[i].type
                value = tok[i].value

                funcbody.append(Token(type_, value))
                
                if type_ == TokenType.OPERATOR and value == '}': in_body = False;break
                
                i+=1
                
        else: Error(self.filename, 'error', "expected '{' to start subroutine body.", 1, True)
                
        
        if len(funcbody) != 0:
            if funcbody[-1].type == TokenType.OPERATOR and funcbody[-1].value == '}':
                funcbody.pop(-1)
                
        # print(funcbody)
        function_body_ast = self.ParseFunctionBody(funcbody, funcretype)
        
        if funcname == 'main':
            self.ast.root.name = "__main_start"

        function_node = FunctionNode(funcname, NodeType.FUNCTION, final_args, func_file_scope_type, funcretype, function_body_ast)
        return function_node, i

    def ParseFunctionBody(self, funcbody, retype):
        self.infun = True
        function_body_ast = Ast()
        function_body_ast.set_root("__func_body_start", "funcbody")
        rt = function_body_ast.root
        
        i = 0
        while i < len(funcbody):
            # print('2323')
            statement = funcbody[i]
            
            if statement.type == TokenType.TYPE:
                # print('sddasddasd')
                if self.GetNextToken().type == TokenType.IDENTIFIER:
                    vardecl, a = self.ParseVariableDecl(funcbody[i:])
                    self.ast.add_node(rt, vardecl)
                    
                
                
            
            if statement.type == TokenType.IDENTIFIER:
                if funcbody[i+1].value == "(" and funcbody[i-1].value != "subr":
                    cl = self.ParseFunctionCall(funcbody[i:])
                    # exit(1)
                    function_body_ast.add_node(rt, cl)
                    
            
            
            elif statement.type == TokenType.ASM_CALL:
                asc_ = self.ParseAsmCalls(funcbody[i:])
                function_body_ast.add_node(rt, asc_)
                
            elif statement.type == TokenType.KEYWORD and statement.value == 'return':
                i += 1
                b = i
                type_ = funcbody[b].type
                value = funcbody[b].value
                ret_val = []

                in_semi = True
                while in_semi and not (type_ == TokenType.ENDLINE or value == ';'):
                    # print(type_, value)
                    ret_val.append(Token(type_, value))
                    b += 1

                    # Update type_ and value for the next iteration
                    if b < len(funcbody):
                        type_ = funcbody[b].type
                        value = funcbody[b].value
                    else:
                        break  # Break the loop if we've reached the end of funcbody
                
                if len(ret_val) ==1:
                    lit = self.ParseLiteral(ret_val)

                else:
                    lit = self.ParseLiteral([self.ParseExpression(ret_val)])
                    

                ret_node = Node('return', NodeType.RETURN, lit, retype)
                function_body_ast.add_node(function_body_ast.root, ret_node)


            else:
                # Handle other types of statements as needed
                pass

            i += 1
            
        self.infun = False

        # print(function_body_ast.root)
        return function_body_ast.root
    
    def ParseAsmCalls(self, tokens_):
        i = 1
        instruction = None
        argument = None
        
        stmt = tokens_[i]
        
        if stmt.type == TokenType.IDENTIFIER:
            instruction = [stmt]
            i+=1
            
        stmt = tokens_[i]
            
        if stmt.type == TokenType.IDENTIFIER:
            argument = [stmt]
            i+=1
            
        instruction = self.ParseLiteral(instruction)
        argument = self.ParseLiteral(argument)
        nd = AssemblyCallNode(instruction, NodeType.ASSEMBLY_CALL, argument)
        return nd 
        
    def ParseInclLibs(self, tokens_):
        i = 0
        aspx = 0
        inc_lib_type = None
        inc_lib_name = None
        inc_lib_data = ""
        tok = tokens_[i]
        
        if tok.type == TokenType.KEYWORD:
            tokens_.pop(i)
            
        tok = tokens_[i]
        
        if tok.type == TokenType.ADDRESS:
            inc_lib_type = LibType.INBUILT
            # tokens_.pop(i)
            # i+=1
            
        else:
            inc_lib_type = LibType.USERDEFINED
            inc_lib_name = tok.value
        
                
        i+=1
        aspx+=1
        
        tok = tokens_[i]
        # print(tokens_, "\n", "\n")

        if tok.type == TokenType.STRING and inc_lib_name is None:
            inc_lib_name =tok.value
            
        i+=1
        aspx+=1
        tok = tokens_[i]
        if tok.type == TokenType.ENDLINE:
            if inc_lib_type == LibType.INBUILT:

                return i, inc_lib_name, inc_lib_type
            
    def ParseFunctionCall(self, token_stream):
        i = 0
        method_name = None
        total_args = 0
        arguments = []


        type_ = token_stream[i].type
        value = token_stream[i].value

        if type_ == TokenType.IDENTIFIER: method_name = value 
        
        i+=1
        type_ = token_stream[i].type
        value = token_stream[i].value
        if type_ ==TokenType.OPERATOR and value == '(':
            in_arg = False

        i+=1
        
        type_ = token_stream[i].type
        value = token_stream[i].value
        
        in_arg = True
        while in_arg:
            type_ = token_stream[i].type
            value = token_stream[i].value
            arguments.append(Token(type_, value))
            
            # print(type_, value)
            if type_ == TokenType.ENDLINE or value == ';':
                if token_stream[i-1].type == TokenType.OPERATOR and token_stream[i-1].value == ')': in_arg = False
                
            # else:
            #     Error(self.filename, 'error', "expected ';' (endline operator) to end the function call.", 1)


            if arguments[-1].type == TokenType.ENDLINE and arguments[-1].value == ';': arguments.pop(-1)
            # elif arguments[-2].type == TokenType.OPERATOR and arguments[-2].value == ')': arguments.pop(-2)
            i+=1

        if arguments[-1].type == TokenType.OPERATOR and arguments[-1].value == ')': arguments.pop(-1)
        # print(arguments)

        a = 0
        while a<len(arguments):
            vl = arguments[a].value
            if vl == ',':
                arguments.pop(a)
            a+=1

        if len(arguments)==1:
            # if arguments[0].type == TokenType.IDENTIFIER:
            #     arguments
            arguments = self.ParseLiteral(arguments)
            
        elif len(arguments)==0:
            pass
        else:
            
            arguments = self.ParseExpression(arguments)

        fcall = Node(method_name, NodeType.FUNCTION_CALL, "None", "None", [arguments])
        return fcall