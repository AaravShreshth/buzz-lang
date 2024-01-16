import subprocess
import random
import os
import tempfile
import frontend
from manifest.tokens import *
from manifest.astz import *
from grammer.errors import Error
from backend import asmt
from backend.asmt import *

class assembly_backend(object):

    # Initialize
    def __init__(self, filename, ast, incl_libs):
        
        """
    
        Generates assembly code from AST (Abstract syntax tree)
        provided by the parser.

        Args:
            filename  (str) : The file which is being compiled
            ast       (Ast) : Main AST to be converted into assembly
            incl_libs (list): Included libraries
            
        """
        
        self.ast = ast.root.children
        self.filename = filename
        self.incl_libs = incl_libs
        self.asm_fr = AssemblyObj()
        self._astSTypes = ["__standalone_lib", "__main_start"]
        
        # Pre run checks
        if ast.root.name == "__global_non_symbl":
            Error(self.filename, 'fault', "no entry point `main` was found in the context, if not standalone object, consider adding the symbol.", 1)
        
        elif ast.root.name in self._astSTypes:pass
        else:
            Error(self.filename, 'error', "unidentified ast type `{}`; returning from further execution.".format(ast.root.name), 1)
    # Visit node.type (fgen)
    def asm_fgen(self, _tree:list):
        """
        
        Main visitor that generates the assembly code.

        Args:
            _tree (list): main tree root node.
            
        """
        
        for node in _tree:
            if node.type == NodeType.FUNCTION:
                cd_ = self.asm_subrf(node.name, node.args, node.body, node.file_scope)
                self.asm_fr.define_function(node.name, node.args, 'func', cd_)
                
                
        
    def asm_subrf(self, name , params, body, scope):
        argument_reg = ["rdx", "rcx", "rdi"]
        
        funcname = name
        funcparams = params
        len_fp = len(funcparams)
        funcbody = body.children
        func_scope = scope
        
        
        asm_body = ""
        
        if func_scope == "universal":
            self.asm_fr.add_global_function(funcname)
            
        if len(funcparams) == 1:
            funcparams = funcparams[0]
            # print(funcparams)
            arg_reg = "rdx"
            
        
        for node in funcbody:
            # print(node, '\n')
            if node.type == NodeType.FUNCTION_CALL:
                callee = node.name
                args = node.children
                # print(args)
                
                if callee not in [_f.name for _f in self.asm_fr.defined_functions]:
                    Error(self.filename, 'note', f"implicit declaration - undefined reference to `{callee}`, expecting object in linker.", 0)
                    self.asm_fr.add_external_function_call(callee)
                if len(args) == 1:
                    args = args[0]
                    

                    arg_reg = "rdx"
                    
                    if args != []:
                        if args.st_type.value == 'string':
                            
                            st = self.asm_fr.define_string('arg_str', args.value)  
                            asm_body = self.asm_fr.custom_instruction(asm_body, f"mov {arg_reg}, {st.coded_name}")
                            asm_body = self.asm_fr.custom_instruction(asm_body, f"mov rcx, {st.coded_len_}")
                            
                        if args.st_type.value == 'IDENTIFIER':
                            found = False
                            for v in self.asm_fr.global_variables:
                                if v.name == args.value:
                                    asm_body = self.asm_fr.custom_instruction(asm_body, f"mov {arg_reg}, {v.coded_name}")
                                    asm_body = self.asm_fr.custom_instruction(asm_body, f"mov rcx, {v.coded_len_}")
                                    found = True
                            
                            if not found: Error(self.filename, 'error', f"could not find any declaration for variable `{args.value}`", 1, True)
                                    
                    asm_body = self.asm_fr.add_function_call(asm_body, callee)  
                        
                elif len(args) == 0:
                    pass
                
                
            elif node.type == NodeType.ASSEMBLY_CALL:
                cal_id = node.name 
                ar = node.arguments
                
                if cal_id.value == 'inb_write___':
                    len_reg = "rcx"
                    if ar.value == funcparams.name:
                        asm_body = self.asm_fr.define_write_call(asm_body, arg_reg, len_reg)
                
                else: Error(self.filename, 'error', f"unidentified `asm` system call `{cal_id.value}`", 1, True)
                
            elif node.type == NodeType.VARIABLE_DECL:
                var_name = node.name
                var_type = node.st_type
                var_value = node.value
                
                if len(var_value)==1:
                    val=var_value[0].value
                    if var_type == 'string':
                        st = self.asm_fr.define_string(var_name, val)
                    
                   
                
            elif node.type == NodeType.RETURN:
                retype = node.st_type
                retval = node.value.value
                t_reval = node.value.st_type.value
                
                if retype != t_reval: Error(self.filename, 'error', f"the subroutine (function) `{funcname}` has return type of <{retype}> got returned value is of type <{t_reval}>.", 1, True)

                if funcname == 'main':
                    self.asm_fr.exit_call_code = retval
        
        
        asm_body+="ret\n"
        
        return asm_body

        
        
    # Main Generator function (method).
    def asm_generate_code(self, toex):
        if toex:
            self.asm_fr.add_executable_symbol()
            
        self.asm_fgen(self.ast)
                                        
        self.code = self.asm_fr.return_final_code()
        return self.code
    
    # Link all objects and create an executable
    def process_code(self, code, to_executable:bool):
        # print(code)
        
        main_asm_filename = self.filename.replace('bzz', 'asm')
        output_object_name = main_asm_filename.replace('asm', 'o')
        output_binary_name = 'a.out'

        with tempfile.NamedTemporaryFile(suffix='.asm') as tmpasm:
            tmpasm.write(code.encode())    
            tmpasm.flush()

            p1 = subprocess.run(["nasm", "-f", "elf64", tmpasm.name, "-o", f"obj/{output_object_name}"]) 
            
            if p1.returncode != 0:
                Error(self.filename, 'error', f"failed to compile target file, assembler returned with exit status {p1.returncode}.", p1.returncode, True)
            
        obj_folder = os.listdir('obj')
        object_files = []
        for file in obj_folder:
            if file.endswith('.o'):
                object_files.append(os.path.join('obj',file))                
                    
        if to_executable:
            p3 = subprocess.run(["ld", "-m", "elf_x86_64", *object_files , "-o", f"{output_binary_name}"]) 
                        