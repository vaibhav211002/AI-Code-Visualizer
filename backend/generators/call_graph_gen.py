def generate_call_graph(parsed: dict) -> str:
    lines = ["graph TD"]

    all_function_names = {fn["name"] for fn in parsed["functions"]}

    for func in parsed["functions"]:
        caller = func["name"]

        for call in func["calls"]:
            # only show calls to functions defined in the code
            if call in all_function_names:
                lines.append(f'    {caller}["{caller}"] --> {call}["{call}"]')

    if len(lines) == 1:
        lines.append('    A["No internal function calls found"]')

    return "\n".join(lines)