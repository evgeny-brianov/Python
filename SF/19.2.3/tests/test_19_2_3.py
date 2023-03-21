import pytest
from app.calculator import Calculator
#название класса тестов
class TestCalc:
    #метод setup, через который мы подключаем тестируемый обьект Calculator
    def setup(self):
        self.calc = Calculator
#тест правильности умножения (positive)
    def test_mult_calc_correctly(self):
        assert self.calc.multiply(self, 3, 3) == 9

# тест правильности деления (positive)
    def test_div_calc_correctly(self):
        assert self.calc.division(self, 12, 3) == 4

# тест правильности сложения (positive)
    def test_add_calc_correctly(self):
        assert self.calc.adding(self, 2, 2) == 4

# тест правильности вычитания (positive)
    def test_sub_calc_correctly(self):
        assert self.calc.subtraction(self, 10, 3) == 7