import ast
from typing import Dict, List, Tuple, Optional

class ComplexityAnalyzer(ast.NodeVisitor):
    """Analyzes Python code to estimate its time complexity."""
    
    def __init__(self):
        self.loops = []
        self.loop_vars = set()
        self.array_ops = []
        self.current_depth = 0
        self.input_var = None
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Identify the input array parameter name."""
        if node.args.args:
            self.input_var = node.args.args[0].arg
        self.generic_visit(node)
        
    def visit_For(self, node: ast.For) -> None:
        """Analyze for loops to determine their range and nesting."""
        self.current_depth += 1
        
        # Extract loop range information
        range_info = self._analyze_range(node.iter)
        if range_info:
            self.loops.append({
                'depth': self.current_depth,
                'range': range_info,
                'var': self._get_target_name(node.target)
            })
            
        self.generic_visit(node)
        self.current_depth -= 1
        
    def _analyze_range(self, node: ast.Call) -> Optional[Dict]:
        """Analyze range() calls to determine loop bounds."""
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'range':
            args = []
            for arg in node.args:
                if isinstance(arg, ast.Name):
                    if arg.id == 'n' or (self.input_var and arg.id == f'len({self.input_var})'):
                        args.append('n')
                    else:
                        args.append(arg.id)
                elif isinstance(arg, ast.Num):
                    args.append(str(arg.n))
                elif isinstance(arg, ast.BinOp):
                    args.append(self._analyze_binop(arg))
            return {'args': args}
        return None
        
    def _analyze_binop(self, node: ast.BinOp) -> str:
        """Analyze binary operations in loop bounds."""
        if isinstance(node.left, ast.Name):
            left = node.left.id
        elif isinstance(node.left, ast.Num):
            left = str(node.left.n)
        else:
            left = '?'
            
        if isinstance(node.right, ast.Name):
            right = node.right.id
        elif isinstance(node.right, ast.Num):
            right = str(node.right.n)
        else:
            right = '?'
            
        op = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/'
        }.get(type(node.op), '?')
        
        return f"{left}{op}{right}"
    
    def _get_target_name(self, node: ast.Name) -> str:
        """Extract the loop variable name."""
        if isinstance(node, ast.Name):
            self.loop_vars.add(node.id)
            return node.id
        return "unknown"
    
    def estimate_complexity(self) -> str:
        """Estimate the time complexity based on analyzed loops."""
        if not self.loops:
            return "O(n)"  # Linear time as a base case for sorting
            
        # Count nested loops and their ranges
        max_depth = 0
        current_depth = 0
        n_loops = 0
        
        for loop in self.loops:
            if loop['depth'] > current_depth:
                current_depth = loop['depth']
            if current_depth > max_depth:
                max_depth = current_depth
            n_loops += 1
            
        # Make estimation based on loop structure
        if max_depth == 1:
            return "O(n)"
        elif max_depth == 2:
            # Check if it's a typical comparison sort pattern
            if n_loops >= 2:
                return "O(n²)"  # Typical bubble, insertion, selection sort
            return "O(n log n)"  # Optimistic case
        elif max_depth >= 3:
            return "O(n³)"  # Cubic time or worse
            
        return "O(?)"  # Unknown complexity

def analyze_sorting_algorithm(code: str) -> str:
    """
    Analyze a sorting algorithm's code to estimate its time complexity.
    
    Args:
        code (str): The Python code containing the sorting algorithm
        
    Returns:
        str: Estimated time complexity in Big O notation
    """
    try:
        tree = ast.parse(code)
        analyzer = ComplexityAnalyzer()
        analyzer.visit(tree)
        return analyzer.estimate_complexity()
    except SyntaxError:
        return "Invalid code"
    except Exception as e:
        return f"Analysis error: {str(e)}"