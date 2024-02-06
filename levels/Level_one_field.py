from levels.gameClasses.Snake import *


def str_2_vector(str):
    list = str.split(', ')
    list[0] = int(list[0])
    list[1] = int(list[1])
    return Vector2(list)

def level_of_server(start_speed, change_speed, max_speed, players_socket):
    # Сама игра
    print('lvl 2 One field')
    res = Vector2(0,0)
    main_game = MAIN(start_speed, change_speed,max_speed,None,True)

    while True:
        # Прием нажатий клавиш
        for i in range(2):
            sock = players_socket[i]

            try:
                data = sock.recv(1024)
                data = data.decode()
                key = data.split('>')[-2]

                # Обработка нажатий
                if main_game.snake_list[i].direction.y == 0 and main_game.snake_list[i].able_2_change_direction:
                    if key == 'UP':
                        main_game.snake_list[i].direction = Vector2(0, -1)
                        main_game.snake_list[i].able_2_change_direction = False
                    if key == 'DOWN':
                        main_game.snake_list[i].direction = Vector2(0, 1)
                        main_game.snake_list[i].able_2_change_direction = False
                if main_game.snake_list[i].direction.x == 0 and main_game.snake_list[i].able_2_change_direction:
                    if key == 'LEFT':
                        main_game.snake_list[i].direction = Vector2(-1, 0)
                        main_game.snake_list[i].able_2_change_direction = False
                    if key == 'RIGHT':
                        main_game.snake_list[i].direction = Vector2(1, 0)
                        main_game.snake_list[i].able_2_change_direction = False
            except:
                continue
        # Обработка состояния
        for i in range(2):
            if main_game.snake_list[i].speed_update_flag:
                pygame.time.set_timer(SCREEN_UPDATE_list[i], main_game.snake_list[i].speed)
                main_game.snake_list[i].speed_update_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for i in range(2):
                if event.type == SCREEN_UPDATE_list[i] and main_game.snake_list[i].direction:
                    main_game.update(i)
                    main_game.snake_list[i].able_2_change_direction = True
        main_game.update()

        game_over_check = main_game.game_over_check

        for i in range(2):
            # Отправка данных

            # template of data
            # game_over_check||snake1||snake2||fruit||fruit_cut||fruit_t_blue||fruit_t_red>
            # snakei = block1|block2|block3|...
            # fruit_t = fruit1|fruit2|...

            message = str(int(game_over_check)) + '||'# game over
            for j in range(2):
                for block in main_game.snake_list[j].body:
                    message += str(block)[1:-1] + '|'
                message += '|'
            message += str(main_game.fruit.pos)[1:-1]
            message += '||'
            message += str(int(main_game.fruit_cut.fc_check)) + '|'
            message += str(main_game.fruit_cut.pos)[1:-1]
            message += '||'
            for fruit in main_game.array_fruit_t:
                if fruit.team == 'blue':
                    message += str(fruit.pos)[1:-1] + '|'
            if len(main_game.array_fruit_t) == 0:
                message += '|'
            else:
                message += '||'
            for fruit in main_game.array_fruit_t:
                if fruit.team == 'red':
                    message += str(fruit.pos)[1:-1] + '|'
            message += '|' + '>'

            try:
                players_socket[i].send(message.encode())
            except:
                # главный цикл закрое сокет
                # Вывод другого игрока из уровня
                for sock in players_socket:
                    try:
                        message = '1>' # game over = True
                        sock.send(message.encode())
                    except:
                        pass
                # остановка таймеров
                for i in range(2):
                    pygame.time.set_timer(SCREEN_UPDATE_list[i],0)
                return
        if game_over_check:
            # остановка таймеров
            for i in range(2):
                pygame.time.set_timer(SCREEN_UPDATE_list[i], 0)
            return main_game.scores
        clock.tick(framerate)

def level_of_client(sock, team):
    print('lvl 2 client')
    main_game = MAIN(0,0,0, None, True)
    while True:
        key = None
        # Считывание команды с клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    key = 'UP'
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    key = 'DOWN'
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    key = 'LEFT'
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    key = 'RIGHT'

        # Отправка на сервер команды
        if key is not None:
            message = key + '>'
            sock.send(message.encode())
        # Получаем новое состояние
        data = sock.recv(2048)
        data = data.decode()
        data = data.split('>')[-2]
        data = data.split('||')

        game_over = bool(int(data[0]))

        if game_over:
            return

        for i in range(2):
            main_game.snake_list[i].body = data[1+i].split('|')
            for j in range(len(main_game.snake_list[i].body)):
                main_game.snake_list[i].body[j] = str_2_vector(main_game.snake_list[i].body[j])

        main_game.fruit.pos = str_2_vector(data[3])

        temp = data[4].split('|')
        main_game.fruit_cut.fc_check = bool(int(temp[0]))
        main_game.fruit_cut.pos = str_2_vector(temp[1])

        try:
            main_game.array_fruit_t.clear()
            for pos in data[5].split('|'):
                pos = str_2_vector(pos)
                main_game.array_fruit_t.append(FRUIT_t(pos,'blue'))
        except:
            pass
        try:
            for pos in data[6].split('|'):
                pos = str_2_vector(pos)
                main_game.array_fruit_t.append(FRUIT_t(pos, 'red'))
        except:
            pass

        # Рисуем новое состояние
        base_screen_fill()
        main_game.draw_elements()
        pygame.display.update()
