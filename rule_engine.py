class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        """Convert the Node to a dictionary for JSON serialization."""
        if self.type == 'operator':
            return {
                'type': self.type,
                'value': self.value,
                'left': self.left.to_dict() if self.left else None,
                'right': self.right.to_dict() if self.right else None,
            }
        else:
            return {
                'type': self.type,
                'value': self.value,
            }

    def __repr__(self):
        if self.type == 'operator':
            return f"({self.left} {self.value} {self.right})"
        else:
            return str(self.value)

# Function to parse rule string into AST
def create_rule(rule_string):
    # For demonstration, a simple parser. Consider using a library for complex parsing.
    parts = rule_string.split('AND')
    nodes = []
    for part in parts:
        part = part.strip()
        if 'OR' in part:
            or_parts = part.split('OR')
            or_nodes = [Node('operand', value=op.strip()) for op in or_parts]
            node = Node('operator', value='OR', left=or_nodes[0], right=or_nodes[1])
        else:
            node = Node('operand', value=part)
        nodes.append(node)

    # Combine nodes into an AND operation
    if nodes:
        root = Node('operator', value='AND', left=nodes[0], right=nodes[1] if len(nodes) > 1 else None)
        return root
    return None

# Function to combine multiple ASTs into one
def combine_rules(rule_nodes, operator='AND'):
    if not rule_nodes:
        return None
    root = rule_nodes[0]
    for node in rule_nodes[1:]:
        root = Node('operator', value=operator, left=root, right=node)
    return root

# Function to evaluate AST against data
def evaluate_rule(ast, data):
    # Check if the AST is a dictionary and convert it to a Node
    if isinstance(ast, dict):
        ast = Node(ast['type'], ast.get('value'), 
                    left=evaluate_rule(ast['left'], data) if ast.get('left') else None,
                    right=evaluate_rule(ast['right'], data) if ast.get('right') else None)

    # Debug print to check the AST before evaluation
    print(f"Evaluating AST: {ast}")

    if ast.type == 'operand':
        # Safely prepare the expression for eval
        expr = ast.value.replace('=', '==')  # Ensure single '=' becomes '=='
        try:
            return eval(expr, {}, data)
        except SyntaxError as e:
            print(f"Syntax error in expression: {expr} - {e}")
            return False
    elif ast.type == 'operator':
        left_eval = evaluate_rule(ast.left, data) if ast.left else False
        right_eval = evaluate_rule(ast.right, data) if ast.right else False
        if ast.value == 'AND':
            return left_eval and right_eval
        elif ast.value == 'OR':
            return left_eval or right_eval
    return False
