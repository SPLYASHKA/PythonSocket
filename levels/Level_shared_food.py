from levels.gameClasses.Snake import *


def str_2_vector(str):
    list = str.split(', ')
    list[0] = int(list[0])
    list[1] = int(list[1])
    return Vector2(list)

def level_sf_server(start_speed, change_speed, max_speed, players_socket):
    # Сама игра
    print('lvl 1 Shared food')
    game_over_check = False
    res = Vector2(0,0)
    game_list = [MAIN(start_speed,change_speed,max_speed),MAIN(start_speed,change_speed,max_speed)]

    while True:
        # Прием нажатий клавиш
        for i in range(2):
            sock = players_socket[i]

            try:
                data = sock.recv(1024)
                data = data.decode()
                key = data.split('>')[-2]

                # Обработка нажатий
                if game_list[i].snake.direction.y == 0 and game_list[i].snake.able_2_change_direction:
                    if key == 'UP':
                        game_list[i].snake.direction = Vector2(0, -1)
                        game_list[i].snake.able_2_change_direction = False
                    if key == 'DOWN':
                        game_list[i].snake.direction = Vector2(0, 1)
                        game_list[i].snake.able_2_change_direction = False
                if game_list[i].snake.direction.x == 0 and game_list[i].snake.able_2_change_direction:
                    if key == 'LEFT':
                        game_list[i].snake.direction = Vector2(-1, 0)
                        game_list[i].snake.able_2_change_direction = False
                    if key == 'RIGHT':
                        game_list[i].snake.direction = Vector2(1, 0)
                        game_list[i].snake.able_2_change_direction = False
            except:
                continue

        # Обработка состояния
        if game_list[0].snake.speed_update_flag or game_list[1].snake.speed_update_flag:
            if game_list[0].snake.speed > game_list[1].snake.speed:
                game_list[0].snake.speed = game_list[1].snake.speed
            else:
                game_list[1].snake.speed = game_list[0].snake.speed
            pygame.time.set_timer(SCREEN_UPDATE, game_list[0].snake.speed)
            game_list[0].snake.speed_update_flag = False
            game_list[1].snake.speed_update_flag = False

        counter1 = game_list[0].snake.snack_counter
        counter2 = game_list[1].snake.snack_counter


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for i in range(2):
                if event.type == SCREEN_UPDATE and game_list[i].snake.direction != Vector2(0, 0):
                    game_list[i].update()
                    game_list[i].snake.able_2_change_direction = True


        if game_list[0].snake.snack_counter - counter1 > 0:
            game_list[1].snake.add_block()
        if game_list[1].snake.snack_counter - counter2 > 0:
            game_list[0].snake.add_block()

        if game_list[0].game_over_check: # Первый проиграл
            game_over_check = True
            res += (0, 1)
        if game_list[1].game_over_check: # Не elif потому что возможна ничья
            game_over_check = True
            res += (1, 0)

        for i in range(2):
            # Отправка данных

            # template of data
            # game_over_check||snake||fruit||fruit_cut||fruit_t>
            # snake = block1|block2|block3|...
            # fruit_t = fruit1|fruit2|...

            message = str(int(game_over_check)) + '||'# game over
            for block in game_list[i].snake.body:
                message += str(block)[1:-1] + '|'
            message += '|'
            message += str(game_list[i].fruit.pos)[1:-1]
            message += '||'
            message += str(int(game_list[i].fruit_cut.fc_check)) + '|'
            message += str(game_list[i].fruit_cut.pos)[1:-1]
            message += '||'
            for fruit in game_list[i].array_fruit_t:
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
                pygame.time.set_timer(SCREEN_UPDATE, 0) # остановка таймера (иначе смешно)
                return
        if game_over_check:
            pygame.time.set_timer(SCREEN_UPDATE, 0) # spot timer
            return res
        clock.tick(framerate)

def level_sf_client(sock, team):
    print('lvl 1 client')
    main_game = MAIN(0,0,0, team)
    while True:
        key = None
        # Считывание команды с клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    key = 'UP'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    key = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    key = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    key = 'RIGHT'

        # Отправка на сервер команды
        if key is not None:
            message = key + '>'
            sock.send(message.encode())

        # Получаем новое состояние
        data = sock.recv(2048)
        data = data.decode()
        print(data)
        data = data.split('>')[-2]
        data = data.split('||')
        print(data)

        game_over = bool(int(data[0]))

        if game_over:
            return

        main_game.snake.body = data[1].split('|')
        for i in range(len(main_game.snake.body)):
            main_game.snake.body[i] = str_2_vector(main_game.snake.body[i])

        main_game.fruit.pos = str_2_vector(data[2])

        temp = data[3].split('|')
        main_game.fruit_cut.fc_check = bool(int(temp[0]))
        main_game.fruit_cut.pos = str_2_vector(temp[1])

        try:
            main_game.array_fruit_t.clear()
            for pos in data[4].split('|'):
                pos = str_2_vector(pos)
                main_game.array_fruit_t.append(FRUIT_t(pos, team))
        except:
            pass

        # Рисуем новое состояние
        base_screen_fill()
        main_game.draw_elements()
        pygame.display.update()