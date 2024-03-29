import tkinter as tk
from random import randint

WIDTH, HEIGHT = 450, 380
DT = 0.5
GRAVITY_CONST = 3
START_PAUSE = 1000
FRAME_TIME = 20
TANK_RADIUS = 25
MIN_BUBBLE_RADIUS = 30
MAX_BUBBLE_RADIUS = 40
MUZZLE_WIDTH = 10


# ========= Model ==============

class Tank:
    """ Танк, который будет порождать снаряды
        и тем самым сбивать пузыри.
    """

    def __init__(self, x, y, canvas):
        self.r = r = TANK_RADIUS
        self._muzzle_length = TANK_RADIUS * 2
        self.muzzle_dx = 0
        self.muzzle_dy = -self._muzzle_length
        self.x = x
        self.y = y
        self._canvas = canvas
        self._muzzle_id = canvas.create_line(x, y, x, y + self._muzzle_length, width=MUZZLE_WIDTH)
        self._turret_id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="green")

    def aim(self, event_x, event_y):
        """ Прицеливание дула по направлению к точке (event_x, event_y)
             Используется подобобие треугольников по двум углам.
             muzzle_l / length == muzzle_dx / dx == muzzle_dy / dy
         """
        dx = event_x - self.x
        dy = event_y - self.y
        length = (dx ** 2 + dy ** 2) ** 0.5
        self.muzzle_dx = self._muzzle_length / length * dx
        self.muzzle_dy = self._muzzle_length / length * dy
        self._canvas.coords(self._muzzle_id, self.x, self.y, self.x + self.muzzle_dx, self.y + self.muzzle_dy)

    def can_shoot(self):
        return True  # fixme: хорошо бы считать сколько снарядов осталось

    def shoot(self, x, y):
        self.aim(x, y)
        velocity = 5
        vx = velocity * self.muzzle_dx / self._muzzle_length
        vy = velocity * self.muzzle_dy / self._muzzle_length
        shell = Shell(self.x + self.muzzle_dx, self.y + self.muzzle_dy, vx, vy,
                      MUZZLE_WIDTH // 2, self._canvas)
        return shell


class Shell:
    """ Снаряд, который летит под действием гравитации,
        вылетая за границу экрана просто исчезает
    """

    def __init__(self, x, y, vx, vy, r, canvas):
        self._zombie = False
        self.x = x
        self.y = y
        self._timeout = 200
        self.vx = vx
        self.vy = vy
        self.r = r
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

    def is_zombie(self):
        return self._zombie

    def check_hit(self, target):
        return target.is_inside(self)

    def destroy(self):
        self._zombie = True
        self._canvas.delete(self.id)

    def cause_damage(self, target):
        self.destroy()
        target.destroy()

    def move(self):
        self._timeout -= 1
        if self._timeout < 0:
            self.destroy()
        self._canvas.coords(self.id,
                            self.x - self.r, self.y - self.r,
                            self.x + self.r, self.y + self.r)
        self.x += self.vx * DT
        self.y += self.vy * DT

        if self.x < self.r:
            self.x = self.r
            self.vx = -self.vx
        if self.x > WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        if self.y < self.r:
            self.y = self.r
            self.vy = -self.vy
        if self.y > HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy = -self.vy



class Bubble:
    """ Пузырик, который разрушается снарядом,
        летает без действия гравитации,
        отражается от стенок
        и идеале упруго отталкивается от других
    """

    def __init__(self, x, y, vx, vy, r, canvas):
        self._zombie = False
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="cyan")

    def move(self):
        self._canvas.coords(self.id,
                            self.x - self.r, self.y - self.r,
                            self.x + self.r, self.y + self.r)
        self.x += self.vx * DT
        self.y += self.vy * DT

        if self.x < self.r:
            self.x = self.r
            self.vx = -self.vx
        if self.x > WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        if self.y < self.r:
            self.y = self.r
            self.vy = -self.vy
        if self.y > HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy = -self.vy

    def is_inside(self, other):
        """Проверяет, находятся ли шарики в пересечении (столкновении). """
        dx = self.x - other.x
        dy = self.y - other.y
        squared_distance = dx ** 2 + dy ** 2
        squared_radius_sum = (self.r + other.r) ** 2
        return squared_distance <= squared_radius_sum

    def collide(self, other):
        """ Обмен скоростями при столновении. """
        self.vx, other.vx = other.vx, self.vx
        self.vy, other.vy = other.vy, self.vy
        # FIXME!

    def destroy(self):
        self._zombie = True
        self._canvas.delete(self.id)

    def is_zombie(self):
        return self._zombie


# ========== Control and View =============

class GameRound:
    """ Игровой раунд.
        Здесь в атрибутах содержатся ссылки на:
        1. холст
        2. объект танка
        3. список текущих, "живых" снарядов
        4. список пузыриков
    """

    def __init__(self, canvas, difficulty=1):
        assert difficulty < 10
        self._canvas = canvas
        self._tank = Tank(WIDTH // 2, HEIGHT, self._canvas)
        self._shells = []
        self.bubbles_number = difficulty * 5
        self.bubbles_max_speed = difficulty * 2
        self._targets = []
        for i in range(self.bubbles_number):
            r = randint(MIN_BUBBLE_RADIUS - difficulty,
                        MAX_BUBBLE_RADIUS - difficulty)
            x = randint(r + 1, WIDTH - r - 1)
            y = randint(r + 1, HEIGHT - r - 1)
            vx = randint(-self.bubbles_max_speed, +self.bubbles_max_speed)
            vy = randint(-self.bubbles_max_speed, +self.bubbles_max_speed)
            bubble = Bubble(x, y, vx, vy, r, self._canvas)
            self._targets.append(bubble)

        canvas.bind("<Button - 1>", self._handle_click)  # естественно мой handle_click
        canvas.bind("<Motion>", self._handle_move)
        canvas.after(START_PAUSE, self._handle_frame)

    def _handle_frame(self):
        for target in self._targets:
            target.move()
        # Попарное взаимодействие целей друг с другом
        for i in range(len(self._targets) - 1):
            for k in range(i + 1, len(self._targets)):
                target_1 = self._targets[i]
                target_2 = self._targets[k]
                if target_1.is_inside(target_2):
                    target_1.collide(target_2)
        
        for shell in self._shells:
            shell.move()
        
        for shell in self._shells:
            for target in self._targets:
                if shell.check_hit(target):
                    shell.cause_damage(target)
        
        for target in self._targets:
            if target.is_zombie():
                self._targets.remove(target)

        self._canvas.after(FRAME_TIME, self._handle_frame)


    def _handle_move(self, event):
        print("handle_move")
        self._tank.aim(event.x, event.y)

    def _handle_click(self, event):
        print("handle click")
        if self._tank.can_shoot():
            new_shell = self._tank.shoot(event.x, event.y)
            self._shells.append(new_shell)
        else:
            print("This tank can't shoot")


class MainWindow:
    """ Главное окно.
        Содержит:
        1. ссылку на root = Tk()
        2. ссылку на экземпляр игрового раунда
        3*.ссылки на все необходимые виджеты: кнопку, лэйбл с очками и т.п.
    """

    def __init__(self):
        self._root = tk.Tk()
        self._root.geometry(str(WIDTH + 10) + 'x' + str(HEIGHT + 35))
        self._restart_button = tk.Button(self._root, text="Запустить игру",
                                         command=self._restart_button_handler)
        self._restart_button.pack()
        self._game = None

    def start_game(self):
        canvas = tk.Canvas(self._root, height=HEIGHT, width=WIDTH,
                           background="blue", border=3)
        canvas.pack()
        self._game = GameRound(canvas)

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
