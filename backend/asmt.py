from enum import Enum
import random

class Templates(Enum):
    BITS64 = """
bits 64
    """

class SYSCALLS(Enum):
    WRITE = """
mov rax, 1
mov rdi, 1
mov rsi, CONTEXT
mov rdx, LENGTH
syscall
"""

    EXIT = """
mov rax, 60
mov rdi, [CODE_R]
syscall
"""

class DfString:
    def __init__(self, name, string, scope):
        self.string = string
        self.name = name
        self.nls = ['0ah']
        
        if scope != '':
            self.coded_name = f"{name}{random.randint(200, 300)}"
            self.coded_len_ = f"len{random.randint(10, 800)}"
        else:
            self.coded_name = f"{name}{random.randint(200, 300)}"
            self.coded_len_ = f"len{random.randint(10, 800)}"
            
        
            
        # self.type_ = type_
        self.scope = scope
        
        cnt = self.string.count('\\n')
        self.string = self.string.replace('\\n', '')
        
        for num in range(cnt):
            self.nls.append('0ah')
            
        
    def get_val(self) -> str:
        return f"""
{self.coded_name} db \"{self.string}\", {", ".join(self.nls)}
{self.coded_len_} equ $-{self.coded_name} 
    """

class DfFunction:
    def __init__(self, name:str, params, type_, body):
        self.name = name
        self.params = params
        self.type = type_
        self.body = body
        
    def __repr__(self) -> str:
        return f"""

Function Name: {self.name},
Function Params: {self.params},
Function Type: {self.type},
Function Body: {self.body}
    
"""
        
class AsmSection(object):
    def __init__(self, section_name):
        self.section_name = f"section .{section_name}\n"
        self.section_body = ""
        
        self.section_final_code = ""
        
    def commit_function(self, func:DfFunction):
        self.commit_line(f"{func.name}:")
        self.section_body+=func.body
        
    def commit_line(self, line):
        self.section_body+=f"{line}\n"
        
    def return_section(self) -> str:
        self.section_final_code+=self.section_name
        self.section_final_code+=self.section_body
        
        return self.section_final_code        

class ExternFunction(object):
    def __init__(self, function_name) -> None:
        self.function_name = function_name
        
    def get_val(self):
        return f"extern {self.function_name}\n"
    
class GlobalFunction(object):
    def __init__(self, function_name) -> None:
        self.function_name = function_name
        
    def get_val(self):
        return f"global {self.function_name}\n"
    
    
class AssemblyObj(object):
    def __init__(self):
        self.is_exec = False
        
        # User allowed
        self.exit_call_code = 0
        
        self.text_section = AsmSection("text")
        self.data_section = AsmSection("data")
        self.bssv_section = AsmSection("bss")
        
        self.sections = [self.text_section, self.data_section, self.bssv_section]
        
        self.external_functions = []
        self.globals = []
        
        self.global_variables = []
        self.defined_functions = []
        self.bitsToWrite = "bits 64\n"
        
        self.final_code = ""
        
        
    # Basics
    
    
    def define_function(self, name, params, type_, body):
        funct = DfFunction(name, params, type_, body)
        self.defined_functions.append(funct)
        
    def define_write_call(self, stringToWrite, varnameOrStr, LenOfStr):
        cl = SYSCALLS.WRITE.value
        cl = cl.replace("CONTEXT", varnameOrStr)
        cl = cl.replace("LENGTH", LenOfStr)
        
        stringToWrite+=cl
        return stringToWrite
    
    def define_string(self, name, string_):
        str_ = DfString(name, string_, 'global')
        # print(str_)
        self.global_variables.append(str_)
        
        self.data_section.commit_line(str_.get_val())
        
        return str_
        
    # Custom string appenditure
    def custom_instruction(self, stringToWrite, line):
        stringToWrite+=f"{line}\n"
        return stringToWrite
    
    # add calls
    
    def add_function_call(self, stringToWrite, callee):
        stringToWrite+=f"call {callee}\n"
        return stringToWrite
        
    def add_external_function_call(self, function_name):
        self.external_functions.append(ExternFunction(function_name))
        
    def add_global_function(self, function_name):
        self.globals.append(GlobalFunction(function_name))
        
    def add_executable_symbol(self):
        self.add_global_function("_start")
        self.define_function("_start", [], "int", f"call main\n {SYSCALLS.EXIT.value}")
        self.is_exec = True
    
    
    # Return the final code
    
    def return_final_code(self) -> str:
        self.final_code+=self.bitsToWrite
        
        for extern in self.external_functions:
            self.final_code+=extern.get_val()
            
        for global_ in self.globals:
            self.text_section.commit_line(global_.get_val())
            
        for function in self.defined_functions:
            self.text_section.commit_function(function)
            
        
        if self.is_exec:
            self.data_section.commit_line(f"CODE_R db {self.exit_call_code}") 
        
        
            
        for section in self.sections:
            self.final_code+=section.return_section()
            
        return self.final_code

# if __name__ == "__main__":
#     code = AssemblyObj()
    
#     code.add_external_function_call("write")
#     code.add_executable_symbol()
    
#     code.define_function("main", [], "int", "call write\n")
    
#     print(code.return_final_code())
            
        