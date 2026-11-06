class Stack:


    def __init__(self):
        self.items = []
    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)
    def pop(self):
        if len(self.items) == 0:
            return "Stack Underflow"
        else:
            return self.items.pop()
    def peek(self):
        if len(self.items) == 0:
            return "Stack is empty"
        else:
            return self.items[-1]
def apply_operator(operator_stack, operand_stack):
        operator = operator_stack.pop()


        right_operand = operand_stack.pop()
        left_operand = operand_stack.pop()

        if operator == '+':
            result = left_operand + right_operand
        elif operator == '-':
            result = left_operand - right_operand
        elif operator == '*':
            result = left_operand * right_operand
        elif operator == '/':
            if right_operand == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = left_operand / right_operand
        else:
            raise ValueError("Invalid operator: " + operator)

        operand_stack.push(result)

def tokenize(expression):
        tokens = []
        number = ''
        for char in expression:
            if char.isdigit():
                number += char
                
            else:
                if number:
                    number = int(number)
                    tokens.append(number)
                    number = ''
                if char in "+-*/()":
                    tokens.append(char)

        if number:
            tokens.append(int(number))
        return tokens

def precedence(operator):
        if operator in ('+', '-'):
            return 1
        elif operator in ('*', '/'):
            return 2
        else:
            return -1

def evaluate(expression):
        tokens = tokenize(expression)
        operator_stack = Stack()
        operand_stack = Stack()
        expect_operand = True

        for token in tokens:
            if isinstance(token, int):
                if not expect_operand:
                    raise ValueError("Expected operator but found operand")
                operand_stack.push(token)
                expect_operand = False


            elif token in "+-*/":
                if expect_operand:
                    raise ValueError("Expected operand but found operator")
                while not operator_stack.is_empty() and operator_stack.peek() != '(' and precedence(operator_stack.peek()) >= precedence(token):
                  apply_operator(operator_stack, operand_stack)
                operator_stack.push(token)
                expect_operand = True
                

            elif token == '(':
                operator_stack.push(token)
                expect_operand = True

            elif token == ')':

                while not operator_stack.is_empty() and operator_stack.peek() != '(':
                    apply_operator(operator_stack, operand_stack)
                if operator_stack.is_empty():
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Remove '(' from stack
                expect_operand = False
        if expect_operand:
            raise ValueError("Expected operand but found operator at the end of expression")
        

       

        while not operator_stack.is_empty():
            if operator_stack.peek() == '(':
               raise ValueError("Mismatched parentheses")
         
            apply_operator(operator_stack, operand_stack)


        if operand_stack.size() != 1:
            raise ValueError("Invalid expression")
        return operand_stack.pop()

def process_file():
    with open("input.txt", "r") as file:
        lines = file.readlines()
        results = []
        for line in lines:
           line = line.strip()
           if line == "-----":
               results.append("-----")
           else:
               result = evaluate(line)
               results.append(str(result))

    with open("output.txt", "w") as file:
        for result in results:
            file.write(result + "\n")

test_cases = [
    "3 + 5 * 2",
    "(10 + 5) * 2",
    "100 / (5 * 2)",
    "10 - 5 - 2",
    "20 / 5 + 3",
    "10 - (2 + 3) * 4",
    "(3 + 2) * (8 - 4)",
    "10 + * 5",
    "(10 + 5",
    "10 / 0",
    "()",
    "10 +"
]

for expression in test_cases:
    try:
        print(expression, "=", evaluate(expression))
    except ValueError as error:
        print(expression, "-> ERROR:", error)

