import buzz

from manifest.tokens import *
from frontend.lexer import Lexer
from frontend.parser_buzz import *
from grammer.errors import Error

class Preprocesser(object):
    def __init__(self, srcfile, codeOfsrc):
        self.included_sources = []
        self.libs = []
        self.filename = srcfile
        self.srcfile_code = codeOfsrc
                                
    def remove_comments(self, code):            
        code = re.sub(re.compile("/\*.*?\*/", re.DOTALL ) ,"" ,code) # remove all occurance streamed comments (/*COMMENT */)  
        code = re.sub(re.compile("//.*?\n" ) ,"" ,code) # remove all occurance singleline comments (//COMMENT\n )
        
        return code

    def create_module_stmt(self, name, body, path, line_num):
        code_ = f"""
** module \"{os.path.abspath(path)}\" {line_num};
{body}
** endmodule {name} \"{os.path.abspath(path)}\" {line_num};
        """
        
        return code_
    def preprocess_file(self):
        self.srcfile_code = self.remove_comments(self.srcfile_code)
        code = str(self.srcfile_code).splitlines()
        new_code = []  # Use a new list to store modified lines
        line_num = 0

        for line in code:
            line_num += 1

            include_regex = re.compile(r'^assiml @ <(.*)>;$')
            include_regex2 = re.compile(r'^assiml @ "(.*)";$')

            if (m := include_regex.search(line)):
                
                try:
                    path = f"stdlib/{m.group(1)}"
                    with open(path) as f:
                        data_ = f.read()
                        d = Preprocesser(m.group(1), data_).preprocess_file()
                        
                        if m.group(1) not in self.included_sources:
                            new_code.append(d)
                            self.included_sources.append(m.group(1))

                except FileNotFoundError:
                    Error(self.filename, 'error', f"could not find specified module (file) `{m.group(1)}`", 1, True)

            else:
                new_code.append(line)

        final_code = "\n".join(new_code)
        return final_code.strip()
