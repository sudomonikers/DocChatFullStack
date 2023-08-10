def do_basic_math(num1: int | str, num2: int | str, operator: str) -> int:
    num1 = int(num1)
    num2 = int(num2)
    #the following function will take two numbers, and do math on them based on the operator
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2
    else:
        return 42
    
if __name__ == "__main__":
    # example usage
    print(do_basic_math(0, 4, '+'))