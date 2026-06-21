def generate_uml(parsed: dict) -> str:
    lines = ["classDiagram"]

    for cls in parsed["classes"]:
        class_name = cls["name"]

        # inheritance
        for base in cls["bases"]:
            lines.append(f"    {base} <|-- {class_name}")

        lines.append(f"    class {class_name} {{")

        # attributes
        for attr in cls["attributes"]:
            lines.append(f"        - {attr}")

        # methods
        for method in cls["methods"]:
            args = ", ".join(
                arg for arg in method["args"] if arg != "self"
            )
            prefix = "+" if not method["name"].startswith("_") else "-"
            method_name = method["name"]
            lines.append(f"        {prefix} {method_name}({args})")

        lines.append("    }")

    return "\n".join(lines)