import sys
import os
import inspect

from frontend import lexer, parser_buzz, preprocess
from grammer.errors import Error
from manifest.astz import print_tree
from backend  import backend



class Buzz(object):
	def __init__(self) -> None:
		"""
		Main buzz language (compiler class)

		Args:
			(None)
		"""


		self.name = "buzzlang"
		self.version = 1.0
		self.filename = None
		self.to_executable = True

		
	def OpenFile(self, path):
		try:
			with open(path, "r") as f:
				return f.read()
		except:
			print("E: '{}' No such file or directory".format(path))
			sys.exit(1) 
			
			
	def Compile(self, code):
		filename = self.filename
		asm_out = f"{filename}.asm"

		# Pre-Process
		self.preprocesser = preprocess.Preprocesser(self.filename, code)
		
		prc_code = self.preprocesser.preprocess_file()
		# Frontend Processes
		self.Lexer = lexer.Lexer(self.filename)
		manifested_tokens = self.Lexer.Tokenize(prc_code)
		self.Parser = parser_buzz.ZParser(manifested_tokens, self.filename)
		
		tree, included_libraries = self.Parser.Parse()
		
		
		# Backend Processes
		self.asm = backend.assembly_backend(self.filename, tree, included_libraries)
		gen_code = self.asm.asm_generate_code(self.to_executable)
		# print(gen_code)
		self.asm.process_code(gen_code, self.to_executable)


if __name__ == "__main__":
	lang_ = Buzz()
	argv = sys.argv

	if len(argv)<2:
		print("buzz (fatal): No input file specified")
		sys.exit(1)
	else:
		d_ = lang_.OpenFile(argv[1])
		lang_.filename = argv[1]
  
		# try:
		lang_.Compile(d_)
   
		# except Exception as e:
		# 	Error(lang_.filename, 'error', f"a compilation error has occured, returned logs:\n {e}", 1, True)
