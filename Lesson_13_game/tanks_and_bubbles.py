import tkinter as tk
from random import randint

WIDTH, HEIGHT = 450, 380
DT =  0.2
GRAVITY_CONST = 3


# ========= Model ==============

class Tank:
    """ Танк, который будет порождать снаряды
        и тем самым сбивать пузыри.
    """
    pass


class Shell:
    """ Снаряд, который летит под действием гравитации,
        вылетая за границу экрана просто исчезает
    """
    pass


class Bubble:
    """ Пузырик, который разрушается снарядом,
        летает без действия гравитации,
        отражается от стенок
        и идеале упруго отталкивается от других
    """
    pass


# ========== Control and View =============

class GameRound:
    """ Игровой раунд.
        Здесь в атрибутах содержатся ссылки на:
        1. объект танка
        2. список текущих, "живых" снарядов
        3. список пузыриков
    """
    def __init__(self):
        pass


    def handle_next_frame(self):
        pass


    def handle_click(self,event):
        pass

class MainWindow:
    """ Главное окно.
        Содержит:
        1. ссылку на root = Tk()
        2. ссылки на все необходимые виджеты: кнопку, лэйбл с очками и т.п.
        3. ссылку на экземпляр игрового раунда
    """
    def __init__(self):
        pass


    def start_game(self):
        pass


    def _handle_frame(self):
        pass


    def _handle_click(self):
        pass


    def mainloop(self):
        pass
    

def main():
    main_window = MainWindow()
    main_window.mainloop()
    print("Game over!")


main()
