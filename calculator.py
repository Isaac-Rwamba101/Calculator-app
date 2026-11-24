import ast
import operator

# The maths signs our calculator understands
OPERATORS = {
    ast.Add: operator.add,            # 3 + 2
    ast.Sub: operator.sub,            # 3 - 2
    ast.Mult: operator.mul,           # 3 * 2
    ast.Div: operator.truediv,        # 3 / 2
    ast.FloorDiv: operator.floordiv,  # 7 // 2  (whole part)
    ast.Mod: operator.mod,            # 7 % 2   (what is left)
    ast.Pow: operator.pow,            # 2 ** 3  (or 2 ^ 3)
    ast.USub: operator.neg,           # -5
    ast.UAdd: operator.pos,           # +5
}
MAX_POWER = 100  # blocks giant sums like 9**9**9


def evaluate(node):
    """Work out the answer for one piece of the sum."""
    if isinstance(node, ast.Constant):
        value = node.value
        if type(value) in (int, float):
            return value
        raise ValueError("only numbers are allowed")
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = evaluate(node.left)
        right = evaluate(node.right)
        if type(node.op) is ast.Pow and abs(right) > MAX_POWER:
            raise ValueError(f"powers over {MAX_POWER} are blocked")
        return OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate(node.operand))
    raise ValueError("use numbers, brackets and + - * / // % **")


def calculate(text):
    """Turn a typed sum such as '3*65 + 2*60' into an answer."""
    text = text.replace("^", "**")  # people often type ^ for power
    tree = ast.parse(text, mode="eval")
    answer = evaluate(tree.body)
    if isinstance(answer, complex):
        raise ValueError("the answer is not a real number")
    if isinstance(answer, float):
        answer = round(answer, 10)    # 0.1 + 0.2 shows as 0.3
        if answer.is_integer():
            answer = int(answer)      # 300.0 shows as 300
    return answer



def main():
    print("Smart Calculator. Type 'exit' to stop.")
    while True:
        text = input("calc > ").strip()
        if text.lower() in ("exit", "quit"):
            break
        if not text:
            continue
        try:
            print("Answer:", calculate(text))
        except ZeroDivisionError:
            print("You cannot divide by zero.")
        except (SyntaxError, ValueError, TypeError,
                OverflowError) as problem:
            print("I could not work that out:", problem)


if __name__ == "__main__":
    main()
