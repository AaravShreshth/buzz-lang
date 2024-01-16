import re
from grammer.errors import Error
from manifest import tokens, expr
from manifest.tokens import Token


class Lexer(object):
    def __init__(self, filename):
        self.init = True
        self.index = 0
        self.tokens = []
        self.rep_tokens = []
        self.filename = filename

    def Tokenize(self, input_code):
        self.tokens_t = re.findall(tokens.token_patterns, input_code)
        self.tokens_t = [token for token in self.tokens_t if not re.match(tokens.whitespace_pattern, token)]
        
        
        while (self.index<len(self.tokens_t)):
            wrd_i = self.tokens_t[self.index]

            if wrd_i in tokens.keywords:
                self.tokens.append(Token(tokens.TokenType.KEYWORD, wrd_i))
                
            elif wrd_i in tokens.logical_ops:
                if wrd_i == '**':   
                    self.tokens.append(Token(tokens.TokenType.FLAG, self.tokens_t[self.index+1]))
                    self.index+=1
                    

            elif wrd_i == ":":
                if self.GetNextToken() == ":":
                    self.tokens.append(Token(tokens.TokenType.ASM_CALL, str(wrd_i)+self.GetNextToken()))
                    self.index+=1
                    
                else:
                    self.tokens.append(Token(tokens.TokenType.OPERATOR, wrd_i))

            elif wrd_i in tokens.types:
                
                self.tokens.append(Token(tokens.TokenType.TYPE, wrd_i))

            elif wrd_i in tokens.premacros:
                self.tokens.append(Token(tokens.TokenType.PREMACRO, wrd_i))

            elif str(wrd_i).startswith(tokens.string_token_t[0]) and str(wrd_i).endswith(tokens.string_token_t[0]):
                self.tokens.append(Token(tokens.TokenType.STRING, wrd_i[1:-1]))


            elif re.match(tokens.identifier_pattern, wrd_i):
                self.tokens.append(Token(tokens.TokenType.IDENTIFIER, wrd_i))

            elif str(wrd_i).isdigit():
                self.tokens.append(Token(tokens.TokenType.INTEGER, wrd_i))

            elif expr.isFloat(wrd_i):
                self.tokens.append(Token(tokens.TokenType.FLOAT, wrd_i))

            elif wrd_i in tokens.operators and wrd_i != tokens.operators[5] and wrd_i != tokens.operators[18]:
                self.tokens.append(Token(tokens.TokenType.OPERATOR, wrd_i))

            elif wrd_i == tokens.operators[5]:
                self.tokens.append(Token(tokens.TokenType.ENDLINE, wrd_i))
                
            elif wrd_i == tokens.operators[18]:
                self.tokens.append(Token(tokens.TokenType.ADDRESS, wrd_i))
                
            else:
                Error(self.filename, 'error', f"found unrecognized token `{wrd_i}`; returning from compilation.", 1, True)
                

            self.index+=1

        return self.tokens
    
    def GetNextToken(self):
        return self.tokens_t[self.index+1]
    
    def Reset(self):
        self.tokens = []