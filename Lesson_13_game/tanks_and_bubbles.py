import tkinter as tk
from random import randint

WIDTH, HEIGHT = 450, 380
DT =  0.2
GRAVITY_CONST = 3
START_PAUSE = 1000
FRAME_TIME = 20
TANK_RADIUS = 25


# ========= Model ==============

class Tank:
    """ Танк, который будет порождать снаряды
        и тем самым сбивать пузыри.
    """
    def __init__(self, x, y, canvas):
        self.r =  r = TANK_RADIUS
        self.x = x
        self.y = y
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="darkgreen")

class Shell:
    """ Снаряд, который летит под действием гравитации,
        вылетая за границу экрана просто исчезает
    """
    def __init__(self, x, y, vx, vy, r, canvas):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")


class Bubble:
    """ Пузырик, который разрушается снарядом,
        летает без действия гравитации,
        отражается от стенок
        и идеале упруго отталкивается от других
    """
    def __init__(self, x, y, vx, vy, r, canvas):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="cyan")


# ========== Control and View =============

class GameRound:
    """ Игровой раунд.
        Здесь в атрибутах содержатся ссылки на:
        1. холст
        2. объект танка
        3. список текущих, "живых" снарядов
        4. список пузыриков
    """
    def __init__(self, canvas, difficulty = 1):
        assert difficulty < 10
        self._canvas = canvas
        self._tank = Tank(WIDTH // 2, HEIGHT, self._canvas)
        self._shells = []
        self.bubbles_number = difficulty * 5
        self.bubbles_max_speed = difficulty * 2
        self._targets = []
        for i in range(self.bubbles_number):
            r = randint(10 - difficulty, 25 - difficulty)
            x = randint(r + 1, WIDTH - r - 1)
            y = randint(r + 1, HEIGHT - r - 1)
            Vx = randint(-self.bubbles_max_speed, +self.bubbles_max_speed)
            Vy = randint(-self.bubbles_max_speed, +self.bubbles_max_speed)
            bubble = Bubble(x, y, Vx, Vy, r, self._canvas)
            self._targets.append(bubble)


    def handle_frame(self):
        print("handled_frame")


    def handle_click(self,event):
        print("handled_click")

class MainWindow:
    """ Главное окно.
        Содержит:
        1. ссылку на root = Tk()
        2. ссылку на экземпляр игрового раунда
        3*.ссылки на все необходимые виджеты: кнопку, лэйбл с очками и т.п.
    """
    def __init__(self):
        self._root = tk.Tk()
        self._root.geometry(str(WIDTH + 10)+ 'x' + str(HEIGHT + 35))
        self._restart_button = tk.Button(self._root, text="Запустить игру",
                                         command=self._restart_button_handler)
        self._restart_button.pack()
        self._game = None


    def start_game(self):
        canvas = tk.Canvas(self._root, height = HEIGHT, width = WIDTH,
                               background = "lightblue", border = 3)
        canvas.pack()
        self._game = GameRound(canvas)
        canvas.bind("<Button - 1>", self._handle_click) # естественно мой handle_click
        canvas.after(START_PAUSE, self._handle_frame)

    def _handle_frame(self): # функция делегат, просто пробрасывает информацию дальше
        if self._game is not None:
            self._game.handle_frame()
        self._root.after(FRAME_TIME, self._handle_frame)


    def _handle_click(self, event):
        if self._game is not None:
            self._game.handle_click(event)
    
    
    def _restart_button_handler(self):
        if self._game is None:
            self.start_game()
            print("Запустили игру...")
        else:
            print("Игра уже запущена!")


    def mainloop(self):
        self._root.mainloop()
    

def main():
    main_window = MainWindow()
    main_window.mainloop()
    print("Game over!")


main()
