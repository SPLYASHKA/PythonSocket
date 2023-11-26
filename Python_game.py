from Snake import *
from Records import records_table




def game(start_speed, change_speed, max_speed, change_color):
    main_game = MAIN(start_speed, change_speed, max_speed)
    able_2_change_direction = True
    if change_color:
        main_game.snake.color = alt_snake_color
    while True:
        if main_game.snake.speed_update_flag:
            pygame.time.set_timer(SCREEN_UPDATE, main_game.snake.speed)
            main_game.snake.speed_update_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE and main_game.snake.direction != Vector2(0, 0):
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
        clock.tick(framerate)


def menu():
    change_color = False
    screen_width = cell_size * cell_number
    while True:
        screen.fill(screen_color)
        font = pygame.font.Font("freesansbold.ttf", 30)

        text_normal_color = (255, 255, 255)
        text_easy_color = (100, 100, 255)
        text_hard_color = (255, 50, 100)
        text_reverse_color = (255, 50, 255)
        text_hell_color = (255, 0, 0)

        x_pos = screen_width // 2 - 100
        normal_y = 100
        easy_y = 250
        hard_y = 400
        reverse_y = 550
        hell_y = 700

        text_normal = font.render("Нормально - Нажмите 1", True, text_normal_color)
        text_easy = font.render("Легко - нажмите 2", True, text_easy_color)
        text_hard = font.render("Серьезный геймплей - нажмите 3", True, text_hard_color)
        text_reverse = font.render("Обратный режим - нажмите 4", True, text_reverse_color)
        text_hell = font.render("Ну, это тупо ад - 5", True, text_hell_color)

        # text render
        text_rect_normal = text_normal.get_rect()
        text_rect_normal.center = (x_pos, normal_y)
        screen.blit(text_normal, text_rect_normal)

        text_rect_easy = text_easy.get_rect()
        text_rect_easy.center = (x_pos, easy_y)
        screen.blit(text_easy, text_rect_easy)

        text_rect_hard = text_hard.get_rect()
        text_rect_hard.center = (x_pos, hard_y)
        screen.blit(text_hard, text_rect_hard)

        text_rect_reverse = text_reverse.get_rect()
        text_rect_reverse.center = (x_pos, reverse_y)
        screen.blit(text_reverse, text_rect_reverse)

        text_rect_hell = text_hell.get_rect()
        text_rect_hell.center = (x_pos, hell_y)
        screen.blit(text_hell, text_rect_hell)

        font = pygame.font.Font("freesansbold.ttf", 20)
        text_records = font.render("Нажмите esc, чтобы открыть таблицу рекордов", True, (255, 0, 0))
        text_rect_records = text_records.get_rect()
        text_rect_records = (40, 50)
        screen.blit(text_records, text_rect_records)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:  # color
                change_color = True
            if keys[pygame.K_1]:  # normal
                game(150, 30, 30, change_color)
            elif keys[pygame.K_2]:  # easy
                game(200, 10, 60, change_color)
            elif keys[pygame.K_3]:  # hard
                game(70, 10, 20, change_color)
            elif keys[pygame.K_4]:  # reverse
                game(30, -10,30, change_color)
            elif keys[pygame.K_5]:  # hell
                game(30,1,10, change_color)
            elif keys[pygame.K_ESCAPE]:
                records_table()


if __name__ == '__main__':
    menu()