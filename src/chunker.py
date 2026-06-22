import ast
import os


def extract_calls(node) -> list[str]:
    calls = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
            calls.append(child.func.id)
    return calls


def chunk_file(filepath: str) -> list[dict]:
    with open(filepath) as f:
        source = f.read()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    chunks = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            code = ast.get_source_segment(source, node)
            if code:
                chunks.append({
                    'file_path': filepath,
                    'name': node.name,
                    'code': code,
                    'lineno': node.lineno,
                    'calls': extract_calls(node),
                })
    return chunks


def chunk_directory(root: str) -> list[dict]:
    all_chunks = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith('.py'):
                all_chunks.extend(chunk_file(os.path.join(dirpath, fn)))
    return all_chunks
