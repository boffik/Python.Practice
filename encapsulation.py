"""
Разработайте класс с "полной инкапсуляцией", доступ к атрибутам которого и изменение данных реализуются через вызовы методов. 
В объектно-ориентированном программировании принято имена методов для извлечения данных начинать со слова get (взять), 
а имена методов, в которых свойствам присваиваются значения, – со слова set (установить).
Например, getField, setField.
"""

class NewClass:
    name = ""
    def set_value(self, attr, value):
        self.__setattr__(attr, value)

    def get_value(self, attr):
        self.__getattribute__(attr)

    def __setattr__(self, attr, value):
        if attr == "name":
            self.__dict__[attr] = value
        else:
            raise AttributeError(attr + ' not allowed')

    def __getattribute__(self, attr):
        if attr == "name":
            return object.__getattribute__(self,attr)


a = NewClass()
print(a.name)
a.set_value("name", "foo")
print(a.name)
print(a.get_value("name"))
