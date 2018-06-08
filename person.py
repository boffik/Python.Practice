"""
Описание программы:
Есть класс Person, конструктор которого принимает три параметра 
(не учитывая self) – имя, фамилию и квалификацию специалиста. 
Квалификация имеет значение заданное по умолчанию, равное единице.
У класса Person есть метод, который возвращает строку, включающую в себя всю информацию о сотруднике.
Класс Person содержит деструктор, который выводит на экран фразу "До свидания, мистер …" 
(вместо троеточия должны выводиться имя и фамилия объекта).
В основной ветке программы создайте три объекта класса Person. 
Посмотрите информацию о сотрудниках и увольте самое слабое звено.
В конце программы добавьте функцию input(), 
чтобы скрипт не завершился сам, пока не будет нажат Enter. 
Иначе вы сразу увидите как удаляются все объекты при завершении работы программы.
"""

class Person:
    name = str()
    surname = str()
    qualify = int()
    sex = str()
    def __init__(self, name, surname, qualify = 1, sex='male'):
        self.name = name
        self.surname = surname
        self.qualify = qualify
        self.sex = sex

    def prints(self):
        ls = [self.name, self.surname, str(self.qualify)]
        return str(' '.join(ls))

    def __del__(self):
        ls = [self.name, self.surname]
        if self.sex == 'male':
            text = "Mr. "
        else:
            text = "Mrs. "

        print('Goodbye, ' + text + str(' '.join(ls)))

if __name__ == '__main__':
    a = Person("Sam", "O'Neil", 20)
    b = Person("Scott", "Bradley", 15)
    c = Person("Sara", "O'Connor", 100, "female")

    print(a.prints())
    print(b.prints())
    print(c.prints())
    del(b)
    input('>')
