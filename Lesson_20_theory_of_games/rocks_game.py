GAME_OVER_ROCKS_NUMBER = 16

def game_over(s: int):
    return s >= GAME_OVER_ROCKS_NUMBER

def get_player_action():
    x = int(input("Выберите ход (от 1 до 3):"))
    while x not in {1, 2, 3}:
        x = int(input("Так нельзя! Выберите ход (от 1 до 3):"))
    return x

def apply(s, action):
    if action == 1:
        return s + 1
    elif action == 2:
        return s + 3
    elif action == 3:
        return s * 2
    else:
        raise AssertionError('Такого не должно быть никогда!')

def print_game_state(s):
    print('Теперь в куче', s, 'камней.')

def game_round(s: int):
    """ Запускает и поддерживает игровой раунд,
    спрашивая у игроков ход по очереди,
    печатает позицию на экран (текущее число камней),
    а также автоматически определяет конец игры и победителя.
    s - начальное количество камней
    """
    print_game_state(s)
    current_player = 1
    
    while not game_over(s):
        action = get_player_action()
        s = apply(s, action)
        current_player = 2
        print_game_state(s)
        if game_over(s):
            break
        action = get_player_action()
        s = apply(s, action)
        current_player = 1
        print_game_state(s)
    
    print('Победил игрок', 3 - current_player)

game_round(7)
