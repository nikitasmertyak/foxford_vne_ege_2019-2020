from tkinter import *
from random import *

frame_sleep_time = 10 # задержка между кадрами в миллисекундах
dt = 0.1 # квант игрового времени между кадрами
default_radius = 20
atoms_number = 20

class AtomGreen:
    def __init__(self, canvas):
        self.r = default_radius
        self.x, self.y = self.generate_random_ball_coord()
        self.vx, self.vy = self.generate_random_ball_velocity()
        self.avatar = canvas.create_oval(self.x - self.r, self.y - self.r,
        self.x + self.r, self.y + self.r, fill='green')
        self._canvas = canvas

    def move(self):
        new_x = self.x + self.vx*dt
        new_y = self.y + self.vy*dt
        if new_x < self.r or new_x > screen_width - self.r:
            new_x = self.x # rolling back coordinate!
            self.vx = -self.vx
        if new_y < self.r or new_y > screen_height - self.r:
            new_y = self.y # rolling back coordinate!
            self.vy = -self.vy
        self._canvas.move(self.avatar, new_x - self.x, new_y - self.y)
        self.x, self.y = new_x, new_y

    def generate_random_ball_coord(self):
        x = randint(self.r, screen_width - self.r)
        y = randint(self.r, screen_height - self.r)
        return x, y

    def generate_random_ball_velocity(self):
        vx = randint(-1, 1)
        vy = randint(-1, 1)
        return vx, vy

class AtomRed:
    def __init__(self, canvas):
        self.r = default_radius
        self.x, self.y = self.generate_random_ball_coord()
        self.vx, self.vy = self.generate_random_ball_velocity()
        self.avatar = canvas.create_oval(self.x - self.r, self.y - self.r,
        self.x + self.r, self.y + self.r, fill='red')
        self._canvas = canvas

    def move(self):
        new_x = self.x + self.vx*dt
        new_y = self.y + self.vy*dt
        if new_x < self.r or new_x > screen_width - self.r:
            new_x = self.x # rolling back coordinate!
            self.vx = -self.vx
        if new_y < self.r or new_y > screen_height - self.r:
            new_y = self.y # rolling back coordinate!
            self.vy = -self.vy
        self._canvas.move(self.avatar, new_x - self.x, new_y - self.y)
        self.x, self.y = new_x, new_y

    def generate_random_ball_coord(self):
        x = randint(self.r, screen_width - self.r)
        y = randint(self.r, screen_height - self.r)
        return x, y

    def generate_random_ball_velocity(self):
        vx = randint(-20, +20)
        vy = randint(-20, +20)
        return vx, vy


def check_collision(atom1, atom2):
    """определяет факт столкновения между атомами
    atom1, atom2 — экземпляры класса Atom"""
    return (atom1.x - atom2.x)**2 + (atom1.y - atom2.y)**2 <= (atom1.r + atom2.r)**2


def collide(atom1, atom2):
    dx = atom2.x - atom1.x
    dy = atom2.y - atom1.y
    # n — единичный вектор от центра одного атома до центра другого,
    # он же вектор нормали плоскости столкновения
    nx = dx/(dx**2 + dy**2)**0.5
    ny = dy/(dx**2 + dy**2)**0.5

    # разложение скорости первого атома на компоненту продольную и поперечную оси столкновения
    v1_parallel = atom1.vx*nx + atom1.vy*ny # скалярное произведение скорости atom1 на вектор n
    v1_parallel_x = v1_parallel*nx
    v1_parallel_y = v1_parallel*ny
    v1_perpendicular_x = atom1.vx - v1_parallel_x
    v1_perpendicular_y = atom1.vy - v1_parallel_y

    # разложение скорости второго атома на компоненту продольную и поперечную оси столкновения
    v2_parallel = atom2.vx*nx + atom2.vy*ny # скалярное произведение скорости atom1 на вектор n
    v2_parallel_x = v2_parallel*nx
    v2_parallel_y = v2_parallel*ny
    v2_perpendicular_x = atom2.vx - v2_parallel_x
    v2_perpendicular_y = atom2.vy - v2_parallel_y

    # собираем обратно скорости атомов, сохраняя перпендикулярную компоненту скорости и обменивая поперечные
    atom1.vx = v1_perpendicular_x + v2_parallel_x
    atom1.vy = v1_perpendicular_y + v2_parallel_y
    atom2.vx = v2_perpendicular_x + v1_parallel_x
    atom2.vy = v2_perpendicular_y + v1_parallel_y


class GasStatistics:
    def __init__(self, canvas):
        self._canvas = canvas
        self.histogram_bins = 10
        self.histogram_v_max = 10 # максимальная скорость отображаемая в гистограмме
        self._histogram = [0]*self.histogram_bins
        self._scale_x = (int(canvas["height"]) - 40)/self.histogram_v_max
        self._scale_y = 5
        self._x0 = 15 # местоположение оси координат для графика статистики
        self._y0 = int(canvas["height"]) - 20
        # рисуем на холсте оси координат
        canvas.create_line(self._x0, self._y0, int(canvas["width"])-15, self._y0,
        width=2, fill="blue", arrow=LAST) # ось x
        canvas.create_line(self._x0, self._y0, self._x0, 0 + 15, width=2,
        fill="blue", arrow=LAST) # ось y

    def screen_xy(self, x, y):
        x = self._x0 + x*self._scale_x
        y = self._y0 - y*self._scale_y
        return x, y

    def calculate_histogram(self, atoms):
        self._histogram[:] = [0]*self.histogram_bins
        histogram_bin_dv = self.histogram_v_max/self.histogram_bins
        for atom in atoms:
            v = (atom.vx**2 + atom.vy**2)**0.5
            # определение бина гистограммы, в который попадает данная скорость
            i = int(v/self.histogram_v_max*self.histogram_bins)
            i %= len(self._histogram) # чтобы не было вылета за пределы массива гистограммы
            self._histogram[i] += 1

    def show_histogram(self):
        self._canvas.delete('bin')
        for bin in range(self.histogram_bins):
            x, y = self.screen_xy(bin, self._histogram[bin])
            self._canvas.create_oval(x-5, y-5, x+5, y+5, fill='red', tag='bin')


def time_event():
    # даём возможность подвинуться всем целям
    for atom in atoms:
        atom.move()
    # проверяем столкновения атомов друг с другом
    for i in range(len(atoms)):
        for k in range(i+1, len(atoms)):
            if check_collision(atoms[i], atoms[k]):
                collide(atoms[i], atoms[k])
    stats.calculate_histogram(atoms)
    stats.show_histogram()
    gas_canvas.after(frame_sleep_time, time_event)

root = Tk()
gas_canvas = Canvas(root, width=600, height=600)
gas_canvas.pack(side='left')
screen_width = int(gas_canvas["width"])
screen_height = int(gas_canvas["height"])

statistics_frame = Frame(root)
statistics_canvas = Canvas(statistics_frame, width=400, height=400)
freeze_statistics_button = Button(statistics_frame, text="freeze")
statistics_canvas.pack(side='top')
freeze_statistics_button.pack(side='top')
statistics_frame.pack(side='left')

atoms = [AtomGreen(gas_canvas) for i in range(atoms_number // 2)]
atoms += [AtomRed(gas_canvas) for i in range(atoms_number // 2)]
stats = GasStatistics(statistics_canvas)

time_event() # начинаю циклически запускать таймер
root.mainloop()
