import tkinter as tk
from random import randint

WIDTH, HEIGHT = 450, 380
DT =  1


# ========= Model ==============
class Ball:
    def __init__(self):
        self.image = tk.PhotoImage(file = "ball.png")
        self.width, self.height = self.image.width(), self.image.height()
        assert self.width == self.height, "C такой картинкой не работает."
        self.radius = self.width // 2
        self.x = randint(self.radius, WIDTH - self.radius - 1)
        self.y = randint(self.radius, HEIGHT - self.radius - 1)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.id = canvas.create_image(self.x, self.y, image = self.image)


    # смещение на холсте
    def move(self):
        canvas.coords(self.id, self.x, self.y,)
        self.x += self.vx * DT
        self.y += self.vy * DT
        if self.x <= self.radius:
            self.x = self.radius
            self.vx = - self.vx
        if self.y <= self.radius:
            self.y = self.radius
            self.vy = - self.vy
        if self.x >= WIDTH - self.radius - 1:
            self.x = WIDTH - self.radius - 1
            self.vx = - self.vx
        if self.y >= HEIGHT - self.radius - 1:
            self.y = HEIGHT - self.radius - 1
            self.vy = - self.vy


    def is_inside(self, x, y):
        squared_distance = (self.x - x) ** 2 + (self.y - y) ** 2
        return squared_distance < self.radius * self.radius
            

# ========== Control and View =============
def canvas_click_handler(event):
    # print(event.x, event.y)
    global scores, balls, ball
    ball_to_delete_index = None
    for ball in balls:
        if ball.is_inside(event.x, event.y):
            ball_to_delete =  ball
    if ball_to_delete is not None:
        scores += 60 - ball.radius
        scores_label["text"] = str(scores)
        canvas.delete(ball_to_delete.id)
        balls.remove(ball_to_delete)
        

        


def restart_button_handler():
    global balls
    scores = 0
    scores_label["text"] = str(scores)
    for ball in balls:
        canvas.delete(ball.id)
    balls[:] = [Ball() for i in range(5)]
    


# циклический перезапуск событий
def next_frame_job(n):
    for ball in balls:
        ball.move()
    canvas.after(20, next_frame_job, n + 1)


def initilization():
    global root, canvas, ball_id, scores, scores_label, balls
    root = tk.Tk()
    #root.geometry(f"{WIDTH}x{HEIGHT}")
    #создаём холст
    canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH,
                       background = "lightblue")
    canvas.pack()

    scores = 0
    scores_label = tk.Label(root, text = str(scores))
    scores_label.pack()

    restart_button = tk.Button(root, text = "Перезапустить игру",
                               command = restart_button_handler)
    restart_button.pack()

    balls = [Ball() for i in range(5)]
   

    # привязка событий
    canvas.bind("<Button - 1>", canvas_click_handler)
    canvas.after(200, next_frame_job, 1)


def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
