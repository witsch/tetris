from curses import wrapper, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN
from curses import color_pair, init_pair, COLOR_GREEN, COLOR_BLACK
from time import time
from random import choice, random


start = [2049] * 21 + [4095] * 2
tiles = (
    ('0f00', '8888') * 2, ('0660',) * 4,
    ('0c60', '2640') * 2, ('06c0', '4620') * 2,
    ('0e80', 'c440', '2e00', '4460'), ('0e20', '44c0', '8e00', 'c880'),
    ('0e40', '4c40', '4e00', '4640'))


def show(board, window):
    _, cols = window.getmaxyx()
    x = (cols - 24) // 2
    fmt = '<!{}!>'.format
    for y, line in enumerate(board[1:-2]):
        line = fmt(f'{line:>012b}'[1:-1].replace('1', '[]').replace('0', ' .'))
        window.addstr(y, x, line, color_pair(1))
    window.addstr(y := y + 1, x, fmt('=' * 20), color_pair(1))
    window.addstr(y := y + 1, x, '  ' + '\\/' * 10, color_pair(1))
    window.refresh()


def put(board, tile, x, y):
    board = list(board)
    for offset, line in enumerate(tile):
        mask = int(line, 16) << max(7 - x, 0)
        if mask and board[y + offset] & mask:
            return
        board[y + offset] |= mask
    return board


def down(board, window, delay):
    tile, orientation, y, x = choice(tiles), 0, 0, 3
    stop = time() + delay
    while True:
        updated = put(board, tile[orientation], x, y)
        show(updated, window)
        key = window.getch()
        if key == KEY_RIGHT:
            if put(board, tile[orientation], x + 1, y):
                x += 1
        if key == KEY_LEFT:
            if put(board, tile[orientation], x - 1, y):
                x -= 1
        if key == KEY_DOWN:
            if put(board, tile[orientation], x, y + 1):
                y += 1
        if key == KEY_UP:
            if put(board, tile[(orientation + 1) % 4], x, y):
                orientation = (orientation + 1) % 4
        if time() > stop:
            if not put(board, tile[orientation], x, y + 1):
                return updated
            y += 1
            stop += delay


def main(stdscr):
    init_pair(1, COLOR_GREEN, COLOR_BLACK)
    stdscr.clear()
    stdscr.timeout(10)
    board = start
    while board:
        board = down(board, window=stdscr, delay=0.2)
        while 4095 in board[:-2]:
            board.remove(4095)
            board.insert(0, 2049)


wrapper(main)
