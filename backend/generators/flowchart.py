import ast

def generate_flowchart(source_code: str) -> str:
    tree = ast.parse(source_code)
    
    lines = ["graph TD"]
    node_id = [0]
    
    def new_id():
        node_id[0] += 1
        return f"N{node_id[0]}"
    
    def process_body(body, parent_id):
        prev_id = parent_id
        
        for stmt in body:
            if isinstance(stmt, ast.If):
                cond_id = new_id()
                lines.append(f'    {prev_id} --> {cond_id}{{"{ast.unparse(stmt.test)}"}}')
                
                
                true_id = new_id()
                lines.append(f'    {cond_id} -->|Yes| {true_id}["{get_label(stmt.body[0])}"]')
                process_body(stmt.body[1:], true_id)
                
                if stmt.orelse:
                    false_id = new_id()
                    lines.append(f'    {cond_id} -->|No| {false_id}["{get_label(stmt.orelse[0])}"]')
                    process_body(stmt.orelse[1:], false_id)
                
                prev_id = cond_id

            elif isinstance(stmt, ast.For):
                loop_id = new_id()
                lines.append(f'    {prev_id} --> {loop_id}{{"{ast.unparse(stmt.target)} in {ast.unparse(stmt.iter)}"}}')
                body_id = new_id()
                lines.append(f'    {loop_id} -->|Loop| {body_id}["{get_label(stmt.body[0])}"]')
                process_body(stmt.body[1:], body_id)
                prev_id = loop_id

            elif isinstance(stmt, ast.While):
                loop_id = new_id()
                lines.append(f'    {prev_id} --> {loop_id}{{"{ast.unparse(stmt.test)}"}}')
                body_id = new_id()
                lines.append(f'    {loop_id} -->|Loop| {body_id}["{get_label(stmt.body[0])}"]')
                process_body(stmt.body[1:], body_id)
                prev_id = loop_id

            else:
                stmt_id = new_id()
                lines.append(f'    {prev_id} --> {stmt_id}["{get_label(stmt)}"]')
                prev_id = stmt_id
        
        # End node
        end_id = new_id()
        lines.append(f'    {prev_id} --> {end_id}([End])')

    def get_label(stmt) -> str:
        try:
            return ast.unparse(stmt).replace('"', "'")
        except:
            return "statement"

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_id = new_id()
            lines.append(f'    {start_id}([Start: {node.name}])')
            process_body(node.body, start_id)
            break  

    return "\n".join(lines)