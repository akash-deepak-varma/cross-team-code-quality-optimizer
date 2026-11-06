import ast


class ASTAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.variable_assignments = 0

    def visit_FunctionDef(self, node):
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "end_line": node.end_lineno,
            "parameters": len(node.args.args),
            "lines": node.end_lineno - node.lineno + 1
        })

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.classes.append({
            "name": node.name,
            "line": node.lineno,
            "end_line": node.end_lineno
        })

        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)

    def visit_Assign(self, node):
        self.variable_assignments += len(node.targets)
        self.generic_visit(node)


def analyze_ast(source_code: str):

    tree = ast.parse(source_code)

    analyzer = ASTAnalyzer()
    analyzer.visit(tree)

    return {
        "function_count": len(analyzer.functions),
        "class_count": len(analyzer.classes),
        "import_count": len(analyzer.imports),
        "variable_assignments": analyzer.variable_assignments,
        "functions": analyzer.functions,
        "classes": analyzer.classes
    }