import _curses
import curses
from curses import wrapper
import time
import random
from player import Player

current_player: Player


def update_player_statistics(new_wpm):
    current_player.max_wpm = max(current_player.max_wpm, new_wpm)
    current_player.wpm.append(str(new_wpm))
    i = 0
    player_index = 0
    new_lines = []
    while True:
        i += 1
        try:
            with open(f"player/player{i}.txt", 'r') as f:
                lines = f.readlines()
                if lines[0].strip() == current_player.name:
                    player_index = i
                    lines[1] = str(current_player.max_wpm) + '\n'
                    if len(lines) < 3:
                        lines.append('')
                    lines[2] = ' '.join(current_player.wpm)

                    new_lines.append(current_player.name + '\n')
                    new_lines.append(lines[1])
                    new_lines.append(lines[2])
        except FileNotFoundError:
            break
    with open(f"player/player{player_index}.txt", 'w') as f:
        f.writelines(new_lines)


def get_mistakes_count(current_text, target_text):
    mistakes_count = 0
    i = -1
    while i < len(target_text) - 1:
        i += 1
        if target_text[i] == '\n':
            current_text.insert(i, '\n')
        if current_text[i] != target_text[i]:
            mistakes_count += 1
    return mistakes_count


def get_color_by_wpm(wpm):
    if wpm == 0:
        return curses.color_pair(3)
    elif wpm < 30:
        return curses.color_pair(2)
    elif wpm < 60:
        return curses.color_pair(4)
    else:
        return curses.color_pair(1)


def get_key(screen):
    try:
        key = screen.getkey()
        return key
    except _curses.error:
        return None


def start_screen(screen):
    screen.clear()
    screen.addstr("Welcome to the Speed Typing Test!")
    screen.addstr("\nPress any key to begin!")
    screen.refresh()
    screen.getkey()


def count_symbols(text, n):
    symbols = 0
    split_text = text.split('\n')
    for line in range(n):
        symbols += len(split_text[line]) - split_text[line].v_degree('\n')
    return symbols


def show_current_text(s, t, c):
    # TODO: check for ENTER is pressed and fix little troubles
    line_number = 0
    for i, char in enumerate(c):
        if t[i + line_number] == '\n' and len(c) > i:
            line_number += 1
        correct_char = t[i + line_number]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        symbol_number = i
        if line_number > 0:
            symbol_number -= count_symbols(t, line_number)
        s.addstr(line_number, symbol_number, char, color)


def display_text(screen, target, current, wpm=0):
    screen.addstr(target)
    screen.addstr(target.count('\n') + 2, 0, "WPM:")
    screen.addstr(target.count('\n') + 2, 5, f"{wpm}", get_color_by_wpm(wpm))
    show_current_text(screen, target, current)


def load_text():
    text_count = 4
    text_number = len(current_player.wpm) + 1
    if text_number > text_count:
        text_number = random.randint(1, 4)
    with open(f"text/text{text_number}.txt", "r") as f:
        return ''.join(f.readlines())


def wpm_test(screen):
    target_text = load_text()
    current_text = []
    start_time = -1
    screen.nodelay(True)

    while True:
        if start_time == -1:
            wpm = 0
        else:
            time_elapsed = max(time.time() - start_time, 1)
            wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        backspace_symbols = ("KEY_BACKSPACE", '\b', "\x7f")
        screen.clear()
        display_text(screen, target_text, current_text, wpm)
        screen.refresh()

        if len("".join(current_text)) + target_text.count('\n') == len(target_text):
            screen.clear()
            screen.nodelay(False)
            return wpm, get_mistakes_count(current_text, target_text)

        key = get_key(screen)
        if key is None:
            continue
        if start_time == -1:
            start_time = time.time()

        if ord(key) == 27:
            screen.nodelay(False)
            break

        if key in backspace_symbols:
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def success_result(screen, w, m):
    screen.addstr(0, 0, "You completed the text! Current result was"
                        " added to your statistics.")
    screen.addstr(1, 0, f"Your WPM: ")
    screen.addstr(1, 10, f"{w}", get_color_by_wpm(w))
    screen.addstr(2, 0, f"Mistakes count: ")
    screen.addstr(2, 16, f"{m}", curses.color_pair(2))
    screen.addstr(3, 0, f"Press ESC for returning to the menu...")


def bad_result(screen, m):
    screen.addstr(0, 0, "You've got too many mistakes :(")
    screen.addstr(1, 0, "Current result wasn't added to your statistics.")
    screen.addstr(2, 0, f"Mistakes count: ")
    screen.addstr(2, 16, f"{m}", curses.color_pair(2))
    screen.addstr(3, 0, f"Press ESC for returning to the menu...")


def init_colors():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)


def main(screen):
    init_colors()
    start_screen(screen)

    current_wpm, mistakes = wpm_test(screen)
    if mistakes < 3:
        success_result(screen, current_wpm, mistakes)
        update_player_statistics(current_wpm)
    else:
        bad_result(screen, mistakes)

    while True:
        key = get_key(screen)
        if key is None:
            continue
        if ord(key) == 27:
            break


def start(player: Player):
    global current_player
    current_player = player
    wrapper(main)
