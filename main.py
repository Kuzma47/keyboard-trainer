from player import Player
from trainer import start
from statistics import open_statistics


def get_leaderboard():
    base = get_player_database()
    players_records = {}
    for player in base:
        players_records[player.name] = player.get_average_wpm()
    a = reversed(sorted(players_records.items(), key=lambda item: item[1]))
    i = 1
    print('-' * 35 + '\n'
          'N.\tName\t\tAverage WPM\n'
          + '-' * 35)
    for player, record in list(a):
        print(f'{i}.\t{player}\t\t{record}')
        i += 1


def get_player_statistics(player: Player):
    player_wpm = list(map(int, player.wpm))
    if len(player.wpm) < 2:
        print('\nComplete at least 2 texts for getting access to graphic statistics.\n')
    else:
        open_statistics(player_wpm, player.name)
    print(f'Nickname: {player.name}\n'
          f'WPM record: {player.max_wpm}\n'
          f'Average WPM: {player.get_average_wpm()}\n'
          f'Text counter: {len(player.wpm)}')


def get_player_database():
    base = []
    i = 0
    while True:
        i += 1
        try:
            with open(f"player/player{i}.txt", 'r') as f:
                person = []
                for line in range(3):
                    person.append(f.readline().strip())
                base.append(Player(person[0], int(person[1]), person[2].split()))
        except FileNotFoundError:
            break
    return base


def main_menu(player: Player):
    help_message = '---------------------------------------------------\n' \
                   'Command list:\n' \
                   '>> start : for starting your training\n' \
                   '>> leaderboard : to see leaderboard by maximum wpm\n' \
                   '>> me : to see your statistics\n' \
                   '>> exit : to close app\n' \
                   '---------------------------------------------------'
    print(help_message)
    while True:
        answer = input('>> ')

        if answer == 'start':
            start(player)
        if answer == 'leaderboard':
            get_leaderboard()
        if answer == 'me':
            get_player_statistics(player)
        if answer == 'exit':
            break


def main():
    user_name = input('Enter you nickname: ')
    player_base = get_player_database()
    for player in player_base:
        if user_name == player.name:
            current_player = player
            print(f'Welcome back, {user_name}.')
            break
    else:
        print(f'You was registered as player "{user_name}".')
        with open(f"player/player{len(player_base) + 1}.txt", 'w') as f:
            f.write(f'{user_name}\n0\n')
            current_player = Player(user_name, 0, [])
    main_menu(current_player)


if __name__ == '__main__':
    main()
