import math as m
"""
В конструкторе класса инициируется поле, содержащее количество снежинок, выраженное целым числом.
Класс включает методы перегрузки арифметических операторов: __add__() – сложение, __sub__() – вычитание, __mul__() – умножение, __truediv__() – деление.
В классе код этих методов должен выполнять увеличение или уменьшение количества снежинок на число n или в n раз.
Метод __truediv__() перегружает обычное (/), а не целочисленное (//) деление.
Однако пусть в методе происходит округление значения до целого числа.
Класс включает метод makeSnow(), который принимает сам объект и число снежинок в ряду, а возвращает строку вида "*****\n*****\n*****…", где количество снежинок между '\n' равно переданному аргументу, а количество рядов вычисляется, исходя из общего количества снежинок.
Вызов объекта класса Snow в нотации функции с одним аргументом, должен приводить к перезаписи значения поля, в котором хранится количество снежинок, на переданное в качестве аргумента значение.
"""

class Snow:
    num = int()

    def __init__(self, value = 5):
        self.num = value

    def __call__(self, value):
        self.num = value

    def __add__(self, value):
        self.num += value

    def __sub__(self, value):
        self.num -= value

    def __mul__(self, value):
        self.num *= value

    def __truediv__(self, value):
        self.num = m.ceil(float(self.num) / value)

    def makeSnow(self, value):
        snow_str = ('\n'.join([('*' * int(value)) for _ in range(self.num)]))
        return snow_str


a = Snow()
print('initial value: %i' % a.num)
a + 1
print('add 1: %i' % a.num)
a - 2
print('sub 2: %i' % a.num)
a / 3
print('truediv 3: %i' % a.num)
a * 4
print('mul 4: %i' % a.num)
snow = a.makeSnow(7)
print('makeSnow with 7 * in row and %i rows' % a.num)
print(snow)
b = Snow(3)
print('makeSnow with 10 * in row and %i rows' % b.num)
snow2 = b.makeSnow(10)
print(snow2)
