import socket
from Server_game_set import *
from levels.Level_shared_food import level_sf_server

import time

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

main_socket.bind(('', 5555))
main_socket.setblocking(0)

main_socket.listen(2)

players_sockets = []
clock = pygame.time.Clock()


# usefull functions
def wait_players_readiness(players_sockets, callback_requirement=False):
    print('Ожидание готовности клиентов')
    players_ready = [False, False]
    counter_list = [0, 0]
    time = 0
    if callback_requirement:
        time_limit = 30 * framerate
    else:
        time_limit = 5 * framerate
    while time < time_limit:
        if players_ready[0] and players_ready[1]:
            print('Игроки готовы')
            return 0

        for i in range(2):
            # Recv
            try:
                data = players_sockets[i].recv(1024)
                data = data.decode()
                if data == 'Ready':
                    players_ready[i] = True
                    print('Игрок ' + str(i + 1) + ' готов')
            except:
                pass
        if callback_requirement:
            for i in range(2):
                # Send
                if players_ready[1 - i] and counter_list[i] < 3:
                    try:
                        message = 'Enemy ready' + '>'
                        players_sockets[i].send(message.encode())
                        counter_list[i] += 1
                    except:
                        return -1
        time += 1  # не нужно ограничение в начале
        clock.tick(framerate)
    return 2


def send_enemy_disabled(players_sockets):
    # сообщение клиенту о том, что противник отключился
    for sock in players_sockets:
        try:
            message = '-1'
            sock.send(message.encode())
        except:
            pass

def send_score(players_sockets, game_score):
    print('send_score')
    for sock in players_sockets:
        try:
            print('try')
            message = str(game_score)
            sock.send(message.encode())
        except:
            print('except')
            return -1


def call_lvl(players_sockets, game_score, lvl, start_speed, change_speed, max_speed):
    try:
        game_score += lvl(start_speed, change_speed, max_speed, players_sockets)
    except TypeError:
        wait_players_readiness(players_sockets)
        return -1

    print(game_score)
    wait_players_readiness(players_sockets)
    # Отправка счета
    send_score(players_sockets, game_score)

    # Пауза между лвлами
    time.sleep(5)
    return game_score


# main function
def game():
    # time.sleep(1)
    print('GAME!')
    for i in range(2):
        sock = players_sockets[i]
        try:
            message = 'GAME!||' + str(i) + '>'
            sock.send(message.encode())
        except:
            return -1
    # Готовность
    error = wait_players_readiness(players_sockets, True)
    if error != 0:
        return error

    game_score = Vector2(0, 0)

    # Вызов первого уровня
    call_res = call_lvl(players_sockets, game_score, level_sf_server, 150, 20, 100)
    if call_res == -1:
        return -1
    game_score = call_res

    # Вызов второго уровня TODO Второй лвл
    call_res = call_lvl(players_sockets, game_score, level_sf_server, 150, 20, 100)
    if call_res == -1:
        return -1
    game_score = call_res

    # Вызов третьего уровня TODO Третий лвл
    call_res = call_lvl(players_sockets, game_score, level_sf_server, 150, 20, 100)
    if call_res == -1:
        return -1
    # game_score = call_res
    return 0


# Подключение игроков
run = __name__ == '__main__'
while True:
    # Проверка желающих подключиться
    try:
        new_socket, addr = main_socket.accept()
        print("Подключился ", addr)
        new_socket.setblocking(0)
        players_sockets.append(new_socket)
    except:
        pass

    if len(players_sockets) == 2:
        error = game()
        if error == 0:
            print('Игра прошла без ошибок')
        elif error == -1:
            send_enemy_disabled(players_sockets)
        elif error == 2:
            print('time limit')

    # Проверка клиентов
    for sock in players_sockets:
        try:
            message = '0>'
            sock.send(message.encode())
        except:
            sock.close()
            players_sockets.remove(sock)
            print('Отключился игрок')

    time.sleep(1)
