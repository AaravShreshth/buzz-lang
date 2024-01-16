from dataclasses import dataclass, field  

@dataclass
class Node:
    name: str
    type: str 
    value: str = field(default_factory=str)
    st_type: str = field(default_factory=str)
    children: list = field(default_factory=list)
    
    def add_child(self, node):
        self.children.append(node)
        
@dataclass
class VariableDeclNode:
    name: str
    type: str 
    value: str = field(default_factory=str)
    st_type: str = field(default_factory=str)
    children: list = field(default_factory=list)
    
    def add_child(self, node):
        self.children.append(node)
        
@dataclass
class BinOpNode:
    name: str
    type: str 
    left: list
    right: list
    operation: str
    children: list = field(default_factory=list)
    
    def add_child(self, node):
        self.children.append(node)
        
@dataclass
class FunctionNode:
    name: str
    type: str 
    args: list
    file_scope: str
    return_type: str = field(default_factory=str)
    body: list = field(default_factory=list)
    
    
    def add_child(self, node):
        self.body.append(node)
        
@dataclass
class ArgumentNode:
    name: str
    type: str 
    children: list = field(default_factory=list)
    
    def add_child(self, node):
        self.body.append(node)
        
@dataclass
class AssemblyCallNode:
    name: str
    type: str 
    arguments: str
    children: list = field(default_factory=list)

    def add_child(self, node):
        self.body.append(node)


class Ast:
    def __init__(self):
        self.root = Node('__global_non_symbl', '_expl_start', '<linux>', '_.asm')
        
    def set_start_symbl(self, root):
        self.root = Node(root, 'main', '<linux>', '_.asm')
        
    def set_root(self, root, type):
        self.root = Node(root, type, '<linux>', '.?')
        
    def returnAST(self):
        return self.root.children
        
    def add_node(self, parent, child):
        parent.add_child(child)  
        
    def __repr__(self) -> str:
        return str(self.root)
        
def print_tree(tree, level=0):
    
    for node in tree.children:
        # print(node)
        print("     " * level, node.name, node.type)
        for child in node.children:
            print(child, level + 1)
