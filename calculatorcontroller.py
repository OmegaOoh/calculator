"""
Calculator Controller Module
Provide Controller Class which call the methods of Calculator class
"""


from calculator import Calculator


class CalculatorController:
    @staticmethod
    def get_answer(text: str) -> str:
        """
        Returns The Answer of the expression
        :param text:  to evaluate
        :return: evaluated answer
        """
        return Calculator.calculate(text)

    @staticmethod
    def delete(text: str):
        """
        Deletes the last element from the text
        :param text: Full text to get remove
        :return: Modified Text without the last element
        """
        return Calculator.del_op(text)

    @staticmethod
    def load_func():
        """
        Get all mathematical functions from Calculator Class
        :return:
        """
        return Calculator.get_function()
