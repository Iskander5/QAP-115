import pytest
from test_calculator.calculator_24 import Calculator

class TestCalculator:
    def setup(self):
        self.calc = Calculator()

    def test_multiply(self):
        result = self.calc.multiply(2, 3)
        assert result == 6

    def test_division(self):
        result = self.calc.division(10, 2)
        assert result == 5.0

    def test_subtraction(self):
        result = self.calc.subtraction(8, 3)
        assert result == 5

    def test_adding(self):
        result = self.calc.adding(2, 3)
        assert result == 5

    def teardown(self):
        print('Teardown method executed')