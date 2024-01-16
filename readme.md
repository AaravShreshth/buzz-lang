# 🐝 Buzz Programming Language

<p align="center">
<img src="docs/buzz_icon.png" alt="buzz-logo"  width="120" height="140">
</p>

Buzz is a simple, systems level compiled programming language. (currently under development.)

## 📝 Overview

Buzz aims to combine the performance of a natively compiled language with the simplicity and readability of a systems language.

Some key planned features:

- Intuitive syntax
- Compiles to fast native code
- Support for systems programming
- Lightning fast execution
- Minimal runtime


## 🚀 Current Status

Buzz is currently in the early stages of development.

Current Stage:
- [x] - Create a RAW Tokenizer to take out string tokens from
         a context (file) and provide a token list.

- [x] - Create a Lexer for the lexical anylization of the token
         list, and provide a tokenized version of the RAW string toks.

- [-] - Parse those tokens and check for syntax errors, and finally,
         create a logical representation of the code called the 
         Abstract syntax tree.

- [ ] - Create a assembly code generator that generates assembly code
         from the logical representation of the code (AST) and check 
         for logical errors in the code.

- [ ] - Create a Standard Library for basic IO functions.

- [ ] - Make a optimizer to provide the maximum compiling speed.




## 🛠 Built With

**Language**: Python 3.11

**Tech Stack**:

Custom Components:

- Lexer - Hand-written lexer in Python
- Parser - Recursive descent parser
- Intermediate Code Generator - Custom code generator using Abstract Syntax Trees

- Compiler - Hand-written Buzz to Assembly compiler in Python
- Runtime Library - Custom lightweight runtime in Python



## 💾 Installation
Buzz is still under development and not ready for end users yet. However, for contributing developers, follow these steps to set up the development environment:

## Clone the Repository

Clone the Buzz Git repository to your local machine:

- `git clone https://github.com/yourname/buzz.git
cd buzz`

## Install Dependencies

Buzz relies on Python 3.8 or higher. Install the Python requirements:

- `pip3 install -r requirements.txt`

This will install the compiler, lexer, parser and other dependencies.

## Build from Source
Now compile the Buzz compiler, runtime and other components:

- ` make build `

This will output the main executables into /dist.


## ✍️ Authors

- [Aarav Shreshth](https://www.github.com/AaravShreshth) - Creator and main contributor 

See also the list of [contributors](https://github.com/AaravShreshth/buzz-lang/contributors) who participated in this project.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
