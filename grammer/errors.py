import colorama
import sys

from colorama import Fore, Back, Style

colorama.init(False)

class Counter():
    def __init__(self):
        self.count = 0
        
    def add_count(self):
        self.count+=1
        
    def return_count(self):
        return self.count
    
counter = Counter()

class Error(object):
    def __init__(self, filename, logtype, log, exitcode, final_log:bool=False, tokens:list=[]):
        c = Fore.RED
        

        if logtype == "note":
            c = Fore.LIGHTMAGENTA_EX
            
        elif logtype == "error":
            final_log = True

        elif logtype == "warning":
            c = Fore.YELLOW

        elif logtype == "fault":
            c = Fore.LIGHTYELLOW_EX

        counter.add_count()
        _f = [_.value for _ in tokens]
        
        
        if len(tokens) != 0:
            print(f"""
{Style.BRIGHT}{Fore.WHITE}{filename}: {c}{logtype}{Fore.RESET}{Style.NORMAL}: {log}{Style.RESET_ALL}
  + | {" ".join(_f)}
    | {'~'*len(_f)}
""")

            if final_log:
                print(
        f"""
{Style.BRIGHT}{Fore.WHITE}{counter.return_count()} compiler note(s) omitted with return code [{exitcode}]{Style.RESET_ALL}
        """)
            
            if logtype == "error":
                sys.exit(exitcode)
                
        else:
            print(f"""
{Style.BRIGHT}{Fore.WHITE}{filename}: {c}{logtype}{Fore.RESET}{Style.NORMAL}: {log}{Style.RESET_ALL}""")

            if final_log:
                print(
        f"""
{Style.BRIGHT}{Fore.WHITE}{counter.return_count()} compiler note(s) omitted with return code [{exitcode}]{Style.RESET_ALL}
        """)
            
            if logtype == "error":
                sys.exit(exitcode)
                