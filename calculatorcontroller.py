from calculator import Calculator


class CalculatorController:
    @staticmethod
    def get_answer(text: str) -> str:
        return Calculator.calculate(text)

    @staticmethod
    def delete(text: str):
        return Calculator.del_op(text)

    @staticmethod
    def load_func():
        return Calculator.get_function()
