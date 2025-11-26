# ╔══════════════════════════════════════════════════════╗
# ║   CLASS TEMPLATE                                     ║
# ╚══════════════════════════════════════════════════════╝


class MyClass:
    def __init__(self, attr1, attr2, attr3, attr4, attr5, attr6, attr7, attr8):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3
        self.attr4 = attr4
        self.attr5 = attr5
        self.attr6 = attr6
        self.attr7 = attr7
        self.attr8 = attr8

class MyClass:
    def __init__(self, *args):
        for i, value in enumerate(args, start=1):
            setattr(self, f"attr{i}", value)

    def __str__(self):
        return f"MyClass({', '.join(str(v) for v in self.__dict__.values())})"


# Optional Inheritance Example
class Parent:
    def __init__(self, x):
        self.x = x


class Child(Parent):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y
