import os
import ast
from typing import Dict, Any

def read_file(file_path: str) -> str:
    """Reads the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """Writes content to a file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def analyze_complexity(file_path: str) -> Dict[str, Any]:
    """Analyzes the cyclomatic complexity and structure of a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
        
        complexity = {
            "functions": [],
            "classes": [],
            "total_lines": len(code.splitlines())
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Simple complexity heuristic: number of decision points
                score = 1
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, (ast.If, ast.While, ast.For, ast.And, ast.Or)):
                        score += 1
                complexity["functions"].append({"name": node.name, "complexity": score})
            elif isinstance(node, ast.ClassDef):
                complexity["classes"].append(node.name)
                
        return complexity
    except Exception as e:
        return {"error": str(e)}

# Define tools for the Gemini SDK
tools = [read_file, write_file, analyze_complexity]
