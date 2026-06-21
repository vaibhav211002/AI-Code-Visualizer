import ast 


def parse_code(source_code : str)-> dict:
    tree = ast.parse(source_code)
    
    return {
        "functions" : extract_functions(tree),
        "classes" : extract_classes(tree),
        "imports" : extract_imports(tree),
    }
    
def extract_functions(tree:ast.AST)-> list:
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node ,ast.FunctionDef):
            functions.append({
                "name" : node.name ,
                "args" : [arg.arg for arg in node.args.args],
                "lineno" : node.lineno,
                "calls" : extract_calls(node),
                "has_return" : any(isinstance(n, ast.Return) for n in ast.walk(node)),
            })
    return functions


def extract_classes(tree: ast.AST) -> list:
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
                "methods": extract_functions(node),
                "attributes": extract_attributes(node),
            })
    
    return classes

def extract_calls(func_node: ast.FunctionDef) -> list:
    calls = []
    
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
    
    return list(set(calls))



def extract_imports(tree: ast.AST) -> list:
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    
    return imports


def extract_attributes(class_node: ast.ClassDef) -> list:
    attributes = []
    
    for node in ast.walk(class_node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                    if target.value.id == "self":
                        attributes.append(target.attr)
    
    return list(set(attributes))