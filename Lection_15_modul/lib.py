def house_print(width, height):
    for i in range(width//2):
        print(' ' * (width // 2 - i) + '*' * 2 * i + ' ' * (width // 2 - i))
    for i in range(height - width // 2):
        print("#" * width)

def triangle_print(width):
    for i in range(width + 1):
        print("*" * i)
