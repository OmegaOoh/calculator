""" Module for Calculator
This module provides Calculator class which can be used to calculate string expression
"""


import math

MATH_FUNCTIONS = {'sqrt': 'math.sqrt', 'exp': 'math.exp',
                  'log10': 'math.log10', 'ln':  'ln', 'log2': 'math.log2'}
OPERATOR_REPLACER = {'^': '**', '%': '/100  *', 'mod': '%'}


def ln(x: (int, float)) -> float:
    return math.log(x, math.e)


class Calculator:
    """ Calculator Class to Perform Calculator Operations """
    @staticmethod
    def calculate(expression: str) -> str:
        """ Perform Calculation
        :param expression: string expression to be calculate
        :return: string the result of the calculation
        """
        for i in OPERATOR_REPLACER:
            expression = expression.replace(i, OPERATOR_REPLACER[i])
        for i in MATH_FUNCTIONS:
            expression = expression.replace(i, MATH_FUNCTIONS[i])
        if expression.endswith('/100 *'):
            expression = expression[:-1]
        # Check for Parentheses
        open_p = expression.count('(')
        close_p = expression.count(')')
        while open_p > close_p:
            expression += ')'
            open_p = expression.count('(')
            close_p = expression.count(')')
        try:
            return str(eval(expression))
        except (SyntaxError, ZeroDivisionError):
            return 'Invalid Format'

    @staticmethod
    def del_op(text: str) -> str:
        """ Delete Latest Element from Text
        If the element is function then remove the entire function from the text
        :param text: full text to get remove
        :return: string of modified text
        """
        check_text = text.lower()
        for i in MATH_FUNCTIONS:
            if check_text.endswith(i + "("):
                return text[:-len(i)-1]
        return text[:-1]

    @staticmethod
    def get_function():
        """ Return The list of all mathematical function"""
        return [i for i in MATH_FUNCTIONS]


