import tkinter as tk
from random import randint

WIDTH, HEIGHT = 450, 380


# ========= Model ==============
def ball_init():
    global ball_id, ball_x, ball_y, ball_image, ball_radius
    ball_image = tk.PhotoImage(file = "ball.png")
    ball_width, ball_height = ball_image.width(), ball_image.height()
    assert ball_width == ball_height, "C такой картинкой не работает."
    ball_radius = ball_width // 2
    ball_x = randint(ball_radius, WIDTH - ball_radius)
    ball_y = randint(ball_radius, HEIGHT - ball_radius)
    ball_id = canvas.create_image(ball_x, ball_y, image = ball_image)


# смещение на холсте
def ball_move():
    global ball_x
    canvas.coords(ball_id, ball_x, ball_y,)
    ball_x += 1


# ========== Control and View =============
def canvas_click_handler(event):
    # print(event.x, event.y)
    global scores
    squared_distance = (ball_x - event.x) ** 2 + (ball_y - event.y) ** 2
    if squared_distance < ball_radius * ball_radius:
        print("Ouch!!!")
        scores += 60 - ball_radius
        scores_label["text"] = str(scores)
        canvas.delete(ball_id)
        ball_init()


def restart_button_handler():
    scores = 0
    scores_label["text"] = str(scores)
    canvas.delete(ball_id)
    ball_init()


# циклический перезапуск событий
def next_frame_job(n):
    ball_move()
    canvas.after(20, next_frame_job, n + 1)


def initilization():
    global root, canvas, ball_id, scores, scores_label
    root = tk.Tk()
    #root.geometry(f"{WIDTH}x{HEIGHT}")
    # создаём холст
    canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH,
                       background = "lightblue")
    canvas.pack()

    scores = 0
    scores_label = tk.Label(root, text = str(scores))
    scores_label.pack()

    restart_button = tk.Button(root, text = "Перезапустить игру",
                               command = restart_button_handler)
    restart_button.pack()

    ball_init()

    # привязка событий
    canvas.bind("<Button - 1>", canvas_click_handler)
    canvas.after(200, next_frame_job, 1)


def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
