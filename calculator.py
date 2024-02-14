import math

MATH_FUNCTIONS = {'sqrt': 'math.sqrt', 'exp': 'math.exp',
                  'log10': 'math.log10', 'ln':  'ln', 'log2': 'math.log2'}
OPERATOR_REPLACER = {'^': '**', '%': '/100', 'mod': '%', ')(': ")*("}


class Calculator:
    """ Calculator Class to Perform Calculator Operations """
    @staticmethod
    def calculate(expression: str) -> str:
        """ Perform Calculation """
        for i in OPERATOR_REPLACER:
            expression = expression.replace(i, OPERATOR_REPLACER[i])
        for i in MATH_FUNCTIONS:
            expression = expression.replace(i, MATH_FUNCTIONS[i])
        # Check for Parentheses
        open_p = expression.count('(')
        close_p = expression.count(')')
        while open_p > close_p:
            expression += ')'
            open_p = expression.count('(')
            close_p = expression.count(')')
        try:
            return str(eval(expression))
        except SyntaxError:
            return 'Invalid Format'

    @staticmethod
    def del_op(text: str) -> str:
        """ Delete Latest Element from Text """
        check_text = text.lower()
        for i in MATH_FUNCTIONS:
            if check_text.endswith(i + "("):
                return text[:-len(i)-1]
        return text[:-1]


    def get_function(self):
        return [i for i in MATH_FUNCTIONS]

def ln(x: (int, float)) -> float:
    return math.log(x, math.e)