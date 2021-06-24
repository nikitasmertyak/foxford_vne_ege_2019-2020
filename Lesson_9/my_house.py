from graph import *

WIDTH = 150
HEIGHT = 140

def paint_house(x, y, width, height):
    foundation_height = int(height * 0.1)
    walls_height = int(height * 0.6)
    roof_height = height - foundation_height - walls_height
    foundation_ledge = int(width * 0.05)
    walls_width = width - foundation_ledge * 2
    #paint_foundation(x, y + height, int(width * 1, 1), height * 0.1)
    paint_foundation(x, y + walls_height, width, foundation_height)
    paint_walls(x + foundation_ledge, y, walls_width, walls_height)
    paint_roof(x, y, width, roof_height)


def paint_foundation(x, y, width, height):
    brushColor(80, 50, 0)
    penColor("black")
    rectangle(x, y, x + width, y + height)


def paint_walls(x, y, width, height):
    brushColor(180, 40, 0)
    penColor("black")
    rectangle(x, y, x + width, y + height)


def paint_roof(x, y, width, height):
    brushColor("yellow")
    penColor("black")
    polygon([(x, y), (x + width, y), ((x + width// 2) , (y - height))])


def clear_canvas():
    for item in canvas().find_all():
        canvas().delete(item)



def tick():
    global x, y, scale
    x = x + 2
    y = y - 1
    scale = scale - 0.3
    clear_canvas()
    paint_house(x, y, int(WIDTH * scale / 100), int(HEIGHT * scale / 100))
    

def main():
    global x, y, scale
    x = 150
    y = 150
    scale = 100
    paint_house(x, y, int(WIDTH * scale / 100), int(HEIGHT * scale / 100))
    onTimer(tick, 50)
    run()

main()
