import tkinter as tk

def canvas_click_handler(event):
    print(event.x, event.y)
    squared_distance = (x - event.x) ** 2 + (y - event.y) ** 2
    if squared_distance < r * r:
        print("Ouch!!!")
    # TODO!

# initialization of game
root = tk.Tk() # создать главное окно
root.geometry("450x380")
root.pack_propagate(0)

canvas = tk.Canvas(root) #создадим холст
canvas.pack(fill = "both", expand = True)

x, y = 200, 200
r = 30

oval = canvas.create_oval(x - r, y - r, x + r, y + r, fill = "blue")

canvas.bind("<Button - 1>", canvas_click_handler)

root.mainloop()
