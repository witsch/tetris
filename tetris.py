import curses as crs, random, time


def put(board, tile, shape, x, y, four=(0, 1, 2, 3)):
    masks = [(tile >> ((shape % 4 << 4) + 4 * l) & 0xf) << x for l in four]
    if sum((masks[l] & board[y + l] for l in four)) == 0:
        return board[:y] + [masks[l] | board[y + l] for l in four] + board[y + 4:]


def main(stdscr):
    crs.init_pair(1, crs.COLOR_GREEN, crs.COLOR_BLACK)
    indent = stdscr.getmaxyx()[1] - 24 >> 1
    stdscr.addstr(20, indent, '<!' + '=' * 20 + '!>', crs.color_pair(1))
    stdscr.addstr(21, indent, '  ' + '\\/' * 10, crs.color_pair(1))
    stdscr.timeout(10)
    board = [0xe007] * 21 + [0x1ff8] * 3
    tiles = 0x444400f0444400f0, 0x64400e2044c08e0, 0x88c00e80c4402e0, \
        0x46206c0046206c0, 0x2640c6002640c60, 0x46400e404c404e0, 0x660066006600660
    while board := [0xe007] * board.count(0xffff) + [l for l in board if l != 0xffff]:
        tile, shape, y, x = random.choice(tiles), 0, 0, 6
        stop = time.time() + (delay := 0.2)
        while updated := put(board, tile, shape, x, y):
            for row, line in enumerate(updated[1:-3]):
                line = f'{line:>014b}'[3:-3].replace('1', '[]').replace('0', ' .')
                stdscr.addstr(row, indent, f'<!{line}!>', crs.color_pair(1))
            key = stdscr.getch()
            if key == crs.KEY_LEFT and put(board, tile, shape, x + 1, y):
                x += 1
            if key == crs.KEY_RIGHT and put(board, tile, shape, x - 1, y):
                x -= 1
            if key == crs.KEY_UP and put(board, tile, shape+1, x, y):
                shape += 1
            if (elapsed := time.time() > stop) or key == crs.KEY_DOWN:
                if not put(board, tile, shape, x, y + 1):
                    board = updated
                    break
                y += 1
                stop += delay if elapsed else 0


crs.wrapper(main)
