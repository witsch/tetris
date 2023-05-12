from time import sleep
from random import choice, random


start = [2049] * 21 + [4095] * 2
tiles = (
    ('0f00', '8888') * 2, ('0660',) * 4,
    ('0c60', '2640') * 2, ('06c0', '4620') * 2,
    ('0e80', 'c440', '2e00', '4460'), ('0e20', '44c0', 'c880', '8e00'),
    ('0e40', '4c40', '4e00', '4640'))


def show(board):
    print("\033c", end="\033[A")
    fmt = '<!{}!>'.format
    for line in board[1:-2]:
        print(fmt(f'{line:>012b}'[1:-1].replace('1', '[]').replace('0', ' .')))
    print(fmt('=' * 20))
    print('  ' + '\\/' * 10)


def put(board, tile, x, y):
    board = list(board)
    for offset, line in enumerate(tile):
        mask = int(line, 16) << max(7 - x, 0)
        if mask and board[y + offset] & mask:
            return
        board[y + offset] |= mask
    return board


def down(board):
    tile = choice(tiles)
    orientation = 0
    x = 3
    for y in range(len(board)):
        updated = put(board, tile[orientation], x, y)
        if not updated:
            return put(board, tile[orientation], x, y - 1)
        show(updated)
        if random() < 0.3:
            if put(board, tile[orientation], x + 1, y):
                x += 1
        if random() < 0.3:
            if put(board, tile[orientation], x - 1, y):
                x -= 1
        if random() < 0.15:
            if put(board, tile[(orientation + 1) % 4], x, y):
                orientation = (orientation + 1) % 4
        sleep(0.2)


board = start
while board:
    board = down(board)
