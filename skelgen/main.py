import os
from pathlib import Path
from datetime import date
import argparse

# ==========================
# 템플릿 로딩
# ==========================
TEMPLATE_DIR = Path(__file__).parent / "templates/c"

def load_template(name: str) -> str:
    path = TEMPLATE_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_main_template() -> str:
    template = load_template("main_template.c.tpl")
    return template.replace("{{date}}", str(date.today()))

def generate_source_template(filename: str) -> str:
    module_name = filename.replace(".c", "")
    header_name = f"{module_name}.h"
    template = load_template("source_template.c.tpl")
    return (template.replace("{{filename}}", filename)
                    .replace("{{header_name}}", header_name)
                    .replace("{{module_name}}", module_name)
                    .replace("{{date}}", str(date.today())))

def generate_header_template(filename: str) -> str:
    module_name = filename.replace(".h", "")
    include_guard = f"_{module_name.upper()}_H_"
    template = load_template("header_template.h.tpl")
    return (template.replace("{{filename}}", filename)
                    .replace("{{module_name}}", module_name)
                    .replace("{{include_guard}}", include_guard)
                    .replace("{{date}}", str(date.today())))

# ==========================
# 트리 구조 생성
# ==========================
def build_structure(tree, base_path, author="Unknown"):
    for node in tree:
        path = os.path.join(base_path, node["name"])
        if node["name"].endswith('/'):
            os.makedirs(path, exist_ok=True)
            build_structure(node["children"], path, author)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            ext = os.path.splitext(node["name"])[1].lower()
            content = ""
            # main.c만 별도 처리
            if node["name"] == "main.c":
                content = generate_main_template()
            elif ext == ".h":
                content = generate_header_template(node["name"])
            elif ext == ".c":
                content = generate_source_template(node["name"])
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

# ==========================
# 트리 파싱 (인덴트 or 트리문자)
# ==========================
def parse_tree_structure(lines):
    result = []
    stack = [(0, result)]
    for raw_line in lines:
        line = raw_line.rstrip("\n")
        clean_line = line.replace("├──", "").replace("│", "").replace("└──", "")
        indent = len(line) - len(clean_line)
        clean_line = clean_line.strip()
        if not clean_line:
            continue
        node = {"name": clean_line, "children": []}
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            stack = [(0, result)]
        stack[-1][1].append(node)
        stack.append((indent, node["children"]))
    return result

def parse_indent_structure(lines):
    tree = []
    stack = [( -1, tree)]  # 최상위 들여쓰기 -1로 시작

    for line in lines:
        stripped = line.rstrip('\n')
        if not stripped.strip():
            continue

        indent = len(line) - len(line.lstrip())
        node = {"name": stripped.strip(), "children": []}

        # 현재 indent보다 작은 레벨까지 pop
        while stack and indent <= stack[-1][0]:
            stack.pop()

        # pop 후에도 stack이 비어있으면 최상위에 붙이기
        if not stack:
            stack = [(-1, tree)]

        stack[-1][1].append(node)
        stack.append((indent, node["children"]))

    return tree


# ==========================
# main
# ==========================
def main():
    parser = argparse.ArgumentParser(description="Generate a C project skeleton with template code.")
    parser.add_argument("input", help="Path to the structure file (.txt).")
    parser.add_argument("-o", "--output", default="output", help="Output directory")
    parser.add_argument("--author", default="Unknown", help="Author name for templates")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 트리 구조 자동 판별
    if any(('├' in l or '└' in l or '│' in l) for l in lines):
        structure = parse_tree_structure(lines)
    else:
        structure = parse_indent_structure(lines)

    os.makedirs(args.output, exist_ok=True)
    build_structure(structure, args.output, author=args.author)
    print(f"C skeleton generated successfully in: {args.output}")

if __name__ == "__main__":
    main()
