GAME_OVER_ROCKS_NUMBER = 16

def game_over(s: int):
    return s >= GAME_OVER_ROCKS_NUMBER

def apply(s, action):
    if action == 1:
        return s + 1
    elif action == 2:
        return s + 3
    elif action == 3:
        return s * 2
    else:
        raise AssertionError('Такого не должно быть никогда!')

def value_position(s):
    """ Оценивает позицию s с точки зрения текущего игрока.
        Возвращает:
            -1, если позиция проигрышная
            +1, если выигрышная,
            0, если ничейная (в лучшем случае)
    """
    if s >= 16:
        return -1  # это проигрышные позиции
    min_value = 2  # начальное состояние для поиска минимума
    for action in 1, 2, 3:
        s_after_action = apply(s, action)
        value_of_position_after_action = value_position(s_after_action)
        if value_of_position_after_action < min_value:
            min_value = value_of_position_after_action
    # моя позиция настолько хороша, насколько плохую я нашёл для противника
    return (-min_value)

def get_ai_action(s):
    best_action = None
    min_value = 2  # "плохое", т.е. начальное состояние для поиска минимума
    for action in 1, 2, 3:
        s_after_action = apply(s, action)
        value_of_position_after_action = value_position(s_after_action)
        if value_of_position_after_action < min_value:
            min_value = value_of_position_after_action
            best_action = action
    print("Искусственный интеллект решил",
          "прибавить 1 камень." if best_action == 1 else \
          "прибавить 3 камня." if best_action == 2 else \
          "увеличить к-во камней вдвое!")
    return best_action

def get_player_action(s: int):
    x = int(input("Выберите ход (от 1 до 3):"))
    while x not in {1, 2, 3}:
        x = int(input("Так нельзя! Выберите ход (от 1 до 3):"))
    return x

def print_game_state(s: int):
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
        action = get_player_action(s)
        s = apply(s, action)
        current_player = 2
        print_game_state(s)
        if game_over(s):
            break
        action = get_ai_action(s)
        s = apply(s, action)
        current_player = 1
        print_game_state(s)
    
    print('Победил игрок', 3 - current_player)

game_round(1)
