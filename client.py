import socket
import time

import pygame.event
from levels.Level_shared_food import level_sf_client
from levels.Level_one_field import level_of_client

from Game_set import *


def show_big_text(text, color, size):
    screen_width = cell_size * cell_number

    base_screen_fill()

    font = pygame.font.Font("freesansbold.ttf", size)

    x_pos = screen_width // 2
    y_pos = screen_width // 2

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x_pos, y_pos))
    screen.blit(text_surface, text_rect)

    pygame.display.update()


def show_scores():
    # Прием счета
    data = sock.recv(1024)
    print('Ono reaylno?')
    data = data.decode()
    print(data)
    data = data[:6]
    print(data[:2] + "kkkkk")
    # Проверка на корректность все еще ли играем
    if data[:2] == '-1':
        show_big_text('Соперник отключился', snake_color, 60)
        time.sleep(3)
        return -1

    scores = data
    scores = scores[1:-1]
    scores = scores.split(', ')
    print(scores)
    score_text_blue = scores[0]
    score_text_red = scores[1]

    # Отрисовка
    screen_width = cell_size * cell_number

    base_screen_fill()

    font = pygame.font.Font("freesansbold.ttf", 100)

    score_text_blue_color = blue_snake_color
    score_text_red_color = red_snake_color

    score_text_blue_x_pos = screen_width // 2 - 200
    score_text_red_x_pos = screen_width // 2 + 200
    y_pos = screen_width // 2

    score_surface_blue = font.render(score_text_blue, True, score_text_blue_color)
    score_surface_red = font.render(score_text_red, True, score_text_red_color)

    score_rect_blue = score_surface_blue.get_rect(center=(score_text_blue_x_pos, y_pos))
    score_rect_red = score_surface_red.get_rect(center=(score_text_red_x_pos, y_pos))

    screen.blit(score_surface_blue, score_rect_blue)
    screen.blit(score_surface_red, score_rect_red)

    pygame.display.update()

    return int(score_text_blue), int(score_text_red)


def call_lvl(sock, team, lvl, number):
    lvl(sock, team)
    print('end of lvl ' + str(number))

    # Отправка готовности
    message = 'Ready'
    sock.send(message.encode())

    return show_scores()


# Подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# sock.connect(('localhost',5555))
# sock.connect(('192.168.0.101', 5555))  # локальный ip ноута
sock.connect(('77.232.132.161',5555)) # ip сервера

print('connect')


def game():
    show_big_text('Ожидание второго игрока', snake_color, 40)
    # Проверка подключились ли все игроки, прием номера игрока

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
        data = sock.recv(1024)
        data = data.decode()
        print(data)
        data = data.split('>')[-2]

        if data != '0':
            data = data.split('||')

            if data[1] == '0':
                team = 'blue'
                print(team)
            else:
                team = 'red'
                print(team)

            if data[0] == 'GAME!':
                print('in game')
                break
    # Готовность
    show_big_text('Нажмите пробел', snake_color, 60)
    ready = False
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ready = True
                print('sssss')
        clock.tick(framerate)

    # Отправка готовности
    message = 'Ready'
    sock.send(message.encode())

    # Ожидание готовности соперника
    show_big_text('Ожидание готовности соперника', snake_color, 40)

    enemy_ready = False
    while not enemy_ready:
        print('ya tututututut')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
        data = sock.recv(1024)
        data = data.decode()
        print(data)
        data = data.split('>')[0]
        print(data)
        if data == 'Enemy ready':
            enemy_ready = True
        else:
            show_big_text('Соперник отключился', snake_color, 60)
            time.sleep(3)
            return
        clock.tick(framerate)

    # lvls calls
    levels = [level_sf_client, level_of_client, level_of_client]
    # levels = [level_of_client, level_of_client, level_sf_client]
    call_res = None
    for number, lvl in enumerate(levels, 1):
        call_res = call_lvl(sock, team, lvl, number)
        if call_res == -1:
            return -1
    # for i in range(len(levels)):
    #     lvl = levels[i]
    #     call_res = call_lvl(sock, team, lvl, i + 1)
    #     if call_res == -1:
    #         return -1
    blue_score, red_score = call_res
    time.sleep(2)

    # Вывод итога игры на экран
    if team == 'blue':
        score = blue_score
        enemy_score = red_score
    else:
        score = red_score
        enemy_score = blue_score

    if score > enemy_score:
        print('win')
        win_color = (11, 97, 164)
        show_big_text('Победа', win_color, 100)
    elif score < enemy_score:
        print('def')
        def_color = (246, 1, 24)
        show_big_text('Поражение', def_color, 100)
    else:
        print('draw')
        draw_color = (211, 1, 104)
        show_big_text('Ничья', draw_color, 100)

    time.sleep(5)
    return 0


if __name__ == '__main__':
    while True:
        error = game()
        if error == 1:
            break

pygame.quit()
sys.exit()
