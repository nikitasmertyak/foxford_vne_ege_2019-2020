class Base:
    def __init__(self, x):
        self.x = x
        print("base constructor x = ", x)

    def show(self):
        print("base show, x = ", self.x)

class DerivedA(Base):
    def __init__(self):
        super().__init__("DerivedA")  # Вызов конструктора надкласса
        print("derived A constructor")
