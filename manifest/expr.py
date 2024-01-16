def isFloat(n:str) -> bool:
    
    try:
        float(n)
        return True
    
    except ValueError:
        return False