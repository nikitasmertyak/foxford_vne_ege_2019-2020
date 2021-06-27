import tkinter as tk

WIDTH, HEIGHT = 450, 380


def flier_init():
    global flier, flier_x, flier_y, flier_width, flier_height
    flier_x, flier_y = 50, 25
    flier_width, flier_height = 100, 50
    flier = canvas.create_rectangle(flier_x, flier_y, flier_x + flier_width,
                                    flier_y + flier_height, fill = "blue")


# смещение на холсте
def flier_move():
    global flier_x
    canvas.coords(flier, flier_x, flier_y, flier_x + flier_width,
                                    flier_y + flier_height)
    flier_x += 1


# циклический перезапуск событий
def next_frame_job(n):
    print("frame", n)
    flier_move()
    canvas.after(20, next_frame_job, n + 1)


def initilization():
    global root, canvas, flier
    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH,
                       background = "lightblue")
    canvas.pack()
    flier_init()
    canvas.after(200, next_frame_job, 1)


def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
