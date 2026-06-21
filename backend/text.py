from parser.ast_parser import parse_code
from generators.call_graph_gen import generate_call_graph

code = """
def main():
    login()
    validate()

def login():
    check_credentials()

def validate():
    pass

def check_credentials():
    pass
"""

parsed = parse_code(code)
print(generate_call_graph(parsed))