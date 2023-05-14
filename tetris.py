from curses import wrapper, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN
from curses import color_pair, init_pair, COLOR_GREEN, COLOR_BLACK
from time import time
from random import choice, random


start = [0xe007] * 21 + [0x1ff8] * 2
tiles = (
    ('0f00', '4444') * 2, ('0660',) * 4,
    ('0c60', '2640') * 2, ('06c0', '4620') * 2,
    ('0e80', 'c440', '2e00', '4460'), ('0e20', '44c0', '8e00', 'c880'),
    ('0e40', '4c40', '4e00', '4640'))


def show(board, window):
    _, cols = window.getmaxyx()
    x = (cols - 24) // 2
    fmt = '<!{}!>'.format
    for y, line in enumerate(board[1:-2]):
        line = fmt(f'{line:>014b}'[3:-3].replace('1', '[]').replace('0', ' .'))
        window.addstr(y, x, line, color_pair(1))
    window.addstr(y := y + 1, x, fmt('=' * 20), color_pair(1))
    window.addstr(y := y + 1, x, '  ' + '\\/' * 10, color_pair(1))
    window.refresh()


def put(board, tile, x, y):
    board = list(board)
    for offset, line in enumerate(tile):
        mask = int(line, 16) << x
        if mask and board[y + offset] & mask:
            return
        board[y + offset] |= mask
    return board


def down(board, window, delay):
    tile, orientation, y, x = choice(tiles), 0, 0, 6
    stop = time() + delay
    while True:
        updated = put(board, tile[orientation], x, y)
        show(updated, window)
        key = window.getch()
        if key == KEY_LEFT and put(board, tile[orientation], x + 1, y):
            x += 1
        if key == KEY_RIGHT and put(board, tile[orientation], x - 1, y):
            x -= 1
        if key == KEY_DOWN and put(board, tile[orientation], x, y + 1):
            y += 1
        if key == KEY_UP and put(board, tile[(orientation + 1) % 4], x, y):
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
        board = [0xe007] * board.count(0xffff) + [l for l in board if l != 0xffff]


wrapper(main)
