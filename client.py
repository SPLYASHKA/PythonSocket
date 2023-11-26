import socket
import time

from Snake import *

# Подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost',9090))
sock.setblocking(0)

def Gameee(start_speed, change_speed, max_speed):
    counter = 0
    main_game = MAIN(start_speed, change_speed, max_speed)
    able_2_change_direction = True
    blocks_from_enemy = 0
    while True:
        blocks_from_enemy -= counter
        # Принимаем значение
        try:
            data=sock.recv(1024)
            data = data.decode()
            print('--------------')
            print(data)
            for x in data.split('>'):
                print(x)
                blocks_from_enemy += int(x)
            print('........')
        except:
            pass
        print(blocks_from_enemy)
        counter = main_game.snake.snack_counter
        if main_game.snake.speed_update_flag:
            pygame.time.set_timer(SCREEN_UPDATE, main_game.snake.speed)
            main_game.snake.speed_update_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE and main_game.snake.direction != Vector2(0, 0):
                if blocks_from_enemy > 0:
                    main_game.base_snack_influence()
                    blocks_from_enemy -= 1
                main_game.update()
                able_2_change_direction = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
                if able_2_change_direction:
                    if main_game.snake.direction.y == 0:
                        if event.key == pygame.K_UP:
                            main_game.snake.direction = Vector2(0, -1)
                            able_2_change_direction = False
                        if event.key == pygame.K_DOWN:
                            main_game.snake.direction = Vector2(0, 1)
                            able_2_change_direction = False
                    if main_game.snake.direction.x == 0:
                        if event.key == pygame.K_LEFT:
                            main_game.snake.direction = Vector2(-1, 0)
                            able_2_change_direction = False
                        if event.key == pygame.K_RIGHT:
                            main_game.snake.direction = Vector2(1, 0)
                            able_2_change_direction = False

        # draw all our elements
        screen.fill(screen_color)
        main_game.draw_elements()
        pygame.display.update()
        if main_game.snake.direction == Vector2(0, 0):
            counter = 0
        else:
            counter = main_game.snake.snack_counter - counter
        # отправка на сервер
        if counter > 0:
            message = str(counter) + '>'
            sock.send(message.encode())
        clock.tick(framerate)

if __name__ == '__main__':
    Gameee(150, 20, 100)