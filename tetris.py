from time import sleep
from random import choice, random


empty = '<! . . . . . . . . . .!>\n'
end_1 = '<!====================!>\n'
end_2 = '  ' + '\\/' * 10 + '  '
tiles = (
    (('XXXX',), ('X', 'X', 'X', 'X')),
    (('XX.', ' XX'), ('.X', 'XX', 'X ')),
    (('.XX', 'XX '), ('X.', 'XX', ' X')),
    (('XXX', '  X'), ('.X', '.X', 'XX'), ('X..', 'XXX'), ('XX', 'X ', 'X ')),
    (('XXX', 'X  '), ('XX', ' X', ' X'), ('..X', 'XXX'), ('X.', 'X.', 'XX')),
    (('XXX', ' X '), ('.X', 'XX', ' X'), ('.X.', 'XXX'), ('X.', 'XX', 'X ')),
    (('XX', 'XX'),))


def show(board):
    print("\033c", end="\033[A")
    print(board + end_1 + end_2)


def put(tile, x, y):
    board = empty * 20
    for offset, line in enumerate(tile):
        if y + offset < 20:
            line = line.replace('X', '[]').replace(' ', '.').replace('.', ' .')
            index = x + len(empty) * (y + offset)
            board = board[:index] + line + board[index + len(line):]
    return board


def down():
    tile = choice(tiles)
    orientation = 0
    x = 5
    for y in range(20):
        show(put(tile[orientation], x * 2, y))
        if random() < 0.3:
            x = min(11 - len(tile[orientation]), x + 1)
        if random() < 0.3:
            x = max(1, x - 1)
        if random() < 0.15:
            orientation += 1
            if orientation >= len(tile):
                orientation = 0
        sleep(0.2)


while True:
    down()
