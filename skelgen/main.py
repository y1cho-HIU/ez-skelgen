import os
import argparse
from pathlib import Path

def count_indent(line: str) -> int:
    """Count leading spaces or tabs as indentation level."""
    count = 0
    for ch in line:
        if ch in [' ', '\t']:
            count += 1
        else:
            break
    return count

def create_structure_from_text(file_path: str, output_dir: str = "."):
    """
    Reads a text file describing a project structure and creates corresponding directories and files.
    Example input:
        project/
            include/
                header1.h
                header2.h
            src/
                main.c
                code1.c
                code2.c
            data/
            build/
            makefile
    """
    base_path = Path(output_dir)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f if line.strip()]  # skip blank lines

    stack = [base_path]
    indent_stack = [0]

    for line in lines:
        indent = count_indent(line)
        name = line.strip()

        # 들여쓰기 수준 조정
        while indent < indent_stack[-1]:
            stack.pop()
            indent_stack.pop()
        if indent > indent_stack[-1]:
            stack.append(last_path)
            indent_stack.append(indent)

        current_dir = stack[-1]
        current_path = current_dir / name
        last_path = current_path

        if name.endswith('/'):
            os.makedirs(current_path, exist_ok=True)
            print(f"[DIR]  {current_path}")
        else:
            os.makedirs(current_path.parent, exist_ok=True)
            current_path.touch(exist_ok=True)
            print(f"[FILE] {current_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate a project skeleton from a text structure file.")
    parser.add_argument("input", help="Path to the .txt file describing the project structure.")
    parser.add_argument("-o", "--output", default=".", help="Output directory (default: current directory)")
    args = parser.parse_args()

    create_structure_from_text(args.input, args.output)

if __name__ == "__main__":
    main()
