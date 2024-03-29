from levels.gameClasses.Fruit import *


class SNAKE:
    def __init__(self, start_speed, change_speed, max_speed, team=None):
        self.team = team

        self.start_speed = start_speed
        self.change_speed = change_speed
        self.max_speed = max_speed
        self.able_2_change_direction = True

        if team == 'red':
            print('red')
            self.body_color = red_snake_color
            self.head_color = red_snake_head_color
        elif team == 'blue':
            print('blue')
            self.body_color = blue_snake_color
            self.head_color = blue_snake_head_color
        else:  # Todo переписать не должно быть этого случая
            print('no team')
            self.body_color = snake_color
            self.head_color = snake_head_color


        self.reset()  # Хз стоит ли так делать или лучше как выше

    def draw_snake(self):
        for block in self.body[1:]:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, self.body_color, block_rect)
        block = self.body[0]
        x_pos = int(block.x * cell_size)
        y_pos = int(block.y * cell_size)
        block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        pygame.draw.rect(screen, self.head_color, block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        if self.team == 'red':
            self.body = [Vector2(3, 5), Vector2(3, 4), Vector2(3, 3)]
            self.direction = Vector2(0, 1)
        elif self.team == 'blue':
            self.body = [Vector2(15, 5), Vector2(15, 4), Vector2(15, 3)]
            self.direction = Vector2(0, 1)
        else:
            self.body = [Vector2(3, cell_number / 2), Vector2(2, cell_number / 2), Vector2(1, cell_number / 2)]
            self.direction = Vector2(1, 0)

        self.new_block = False
        self.speed = self.start_speed
        self.speed_update_flag = True
        self.snack_counter = 0
        self.fast = False


class MAIN:
    def __init__(self, start_speed, change_speed, max_speed, team=None, one_field=False, walls_kill=True, cannibalism=False):
        self.one_field = one_field
        if self.one_field:
            self.snake_list = [SNAKE(start_speed, change_speed, max_speed, 'blue'),
                               SNAKE(start_speed, change_speed, max_speed, 'red')]
        else:
            self.snake = SNAKE(start_speed, change_speed, max_speed, team)
        self.fruit = FRUIT()
        self.fruit_cut = FRUIT_cut()
        self.array_fruit_t = []
        self.blocks_from_enemy = 0
        self.game_over_check = False
        if one_field:
            self.scores = Vector2(0, 0)
        self.walls_kill = walls_kill
        self.cannibalism = cannibalism

    def update(self, i=None):
        # move snake
        if not self.one_field:
            self.snake.move_snake()
        elif i is not None:
            self.snake_list[i].move_snake()
            return

        # main:

        # 1.cannibalism
        if self.cannibalism:
            self.check_cannibalism()
        # 2. check fail
        self.check_fail()
        # 3.check snack
        if self.one_field:
            for i in range(2):
                self.check_snack(self.snake_list[i])
        else:
            self.check_snack(self.snake)

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.fruit_cut.draw_fruit()
        if self.one_field:
            for snake in self.snake_list:
                snake.draw_snake()
        else:
            self.snake.draw_snake()
        # funny thing
        for fruit in self.array_fruit_t:
            fruit.draw_fruit_t()

    def base_snake_influence(self, snake):  # todo переписать через это чек снек
        snake.snack_counter += 1
        snake.add_block()
        if snake.speed - snake.change_speed < snake.max_speed:
            snake.fast = True
        else:
            snake.speed -= snake.change_speed
        snake.speed_update_flag = True

    def check_snack(self, snake):
        # regular fruit
        if self.fruit.pos == snake.body[0]:
            self.fruit.randomize()
            self.base_snake_influence(snake)

        for block in snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

        # fruit_cut
        if self.fruit_cut.fc_check:
            if self.fruit_cut.pos == snake.body[0]:
                self.fruit_cut.fc_check = False
                self.generator_fruit_t(snake)
                snake.snack_counter += 2
                self.fruit_cut.randomize()
                snake.speed = (snake.max_speed + snake.start_speed) // 2
                snake.speed_update_flag = True

            for block in snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

        if not (snake.snack_counter % 10 or self.fruit_cut.fc_check):
            self.fruit_cut.fc_check = True

        # fruit_t
        for fruit in self.array_fruit_t:
            if fruit.pos == snake.body[0]:
                self.array_fruit_t.remove(fruit)  # pop
                snake.add_block()
                if snake.speed - snake.change_speed // 2 < snake.max_speed:
                    snake.fast = True
                    snake.speed = snake.max_speed
                else:
                    snake.speed -= snake.change_speed // 2
                snake.speed_update_flag = True

    def generator_fruit_t(self, snake):
        print(snake.team)
        body_copy = snake.body[3:]
        snake.body = snake.body[:3]
        for block in body_copy:
            self.array_fruit_t.append(FRUIT_t(block, snake.team))

    def check_fail(self):
        # границы экрана
        if self.one_field:
            for i in range(2):
                print('aaaa', i)
                print(self.snake_list[i].body[0])
                if not 0 <= self.snake_list[i].body[0].x < cell_number or not 0 <= self.snake_list[i].body[0].y < cell_number:
                    if self.walls_kill:
                        print('tut', i)
                        self.scores += (i, 1-i)
                        self.game_over()
                    else:
                        self.snake_list[i].body[0].x %= cell_number
                        self.snake_list[i].body[0].y %= cell_number
                # Коллизия с собой
                for block in self.snake_list[i].body[1:]:
                    if block == self.snake_list[i].body[0]:
                        self.scores += (i, 1 - i)
                        self.game_over()
        else:
            if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
                if self.walls_kill:
                    self.game_over()
                else:
                    self.snake.body[0].x %= cell_number
                    self.snake.body[0].y %= cell_number

            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.game_over()
        # С другой змеей
        if self.one_field:
            for block in self.snake_list[0].body:
                if block == self.snake_list[1].body[0]:
                    self.scores += (1, 0)
                    self.game_over()
            for block in self.snake_list[1].body:
                if block == self.snake_list[0].body[0]:
                    self.scores += (0, 1)
                    self.game_over()

        if self.one_field:
            # fruit_t
            for i in range(2):
                for fruit in self.array_fruit_t:
                    if fruit.team != self.snake_list[i].team:
                        if fruit.pos == self.snake_list[i].body[0]:
                            self.scores += (i, 1 - i)
                            self.game_over()

        # проверка не съели ли кого-то
        if self.cannibalism:
            for i, snake in enumerate(self.snake_list):
                if len(snake.body) <= 1:
                    self.scores += (i, 1 - i)
                    self.game_over()

    def check_cannibalism(self):
        for i in range(2):
            if self.snake_list[i].body[0] == self.snake_list[1 - i].body[-1]:
                self.snake_list[1 - i].body.pop()
                self.base_snake_influence(self.snake_list[i])

    def game_over(self):
        # бесмертие для dev
        # if not self.one_field:
        #     self.game_over_check = True
        self.game_over_check = True

    def full_reset(self):
        if self.one_field:
            for i in range(2):
                self.snake_list[i].reset()
        else:
            self.snake.reset()
        self.fruit_cut.reset()
        self.array_fruit_t.clear()
