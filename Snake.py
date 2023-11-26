from Fruit import *




class SNAKE:
    def __init__(self, start_speed, change_speed, max_speed):
        self.start_speed = start_speed
        self.change_speed = change_speed
        self.max_speed = max_speed

        self.color = snake_color

        # self.body = [Vector2(3, cell_number / 2), Vector2(2, cell_number / 2), Vector2(1, cell_number / 2)]
        # self.direction = Vector2(0, 0)
        # self.new_block = False
        # self.speed = self.start_speed
        # self.snack_counter = 0
        # self.fast = False
        # self.speed_update_flag = True
        self.reset() # Хз стоит ли так делать или лучше как выше

    def draw_snake(self):
        for block in self.body[1:]:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, self.color, block_rect)
        block = self.body[0]
        x_pos = int(block.x * cell_size)
        y_pos = int(block.y * cell_size)
        block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        pygame.draw.rect(screen, snake_head_color, block_rect)

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
        self.body = [Vector2(3, cell_number / 2), Vector2(2, cell_number / 2), Vector2(1, cell_number / 2)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.speed = self.start_speed
        self.speed_update_flag = True
        self.snack_counter = 0
        self.fast = False


class MAIN:
    def __init__(self, start_speed, change_speed, max_speed):
        self.snake = SNAKE(start_speed, change_speed, max_speed)
        self.fruit = FRUIT()
        self.fruit_cut = FRUIT_cut()
        self.array_fruit_t = []
        self.blocks_from_enemy = 0

    def update(self):
        self.snake.move_snake()
        self.check_snack()
        self.check_fail()
        # print(self.snake.speed)

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.fruit_cut.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        # funny thing
        for fruit in self.array_fruit_t:
            fruit.draw_fruit_t()

    def base_snack_influence(self):
        self.snake.add_block()
        if self.snake.speed - self.snake.change_speed < self.snake.max_speed:
            self.snake.fast = True
        else:
            self.snake.speed -= self.snake.change_speed
        self.snake.speed_update_flag = True
    def check_snack(self):
        # regular fruit
        if self.fruit.pos == self.snake.body[0]:
            self.snake.snack_counter += 1
            self.fruit.randomize()
            self.base_snack_influence()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

        # fruit_cut
        if self.fruit_cut.fc_check:
            if self.fruit_cut.pos == self.snake.body[0]:
                self.fruit_cut.fc_check = False
                self.generator_fruit_t()
                self.snake.snack_counter += 2
                self.fruit_cut.randomize()
                self.snake.speed = (self.snake.max_speed + self.snake.start_speed) // 2
                self.snake.speed_update_flag = True


            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

        if not (self.snake.snack_counter % 10 or self.fruit_cut.fc_check):
            self.fruit_cut.fc_check = True

        # fruit_t
        for fruit in self.array_fruit_t:
            if fruit.pos == self.snake.body[0]:
                self.array_fruit_t.remove(fruit)  # pop
                self.snake.add_block()
                if self.snake.speed - self.snake.change_speed // 2 < self.snake.max_speed:
                    self.snake.fast = True
                    self.snake.speed = self.snake.max_speed
                else:
                    self.snake.speed -= self.snake.change_speed // 2
                self.snake.speed_update_flag = True

            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

    def generator_fruit_t(self):
        body_copy = self.snake.body[3:]
        self.snake.body = self.snake.body[:3]
        for block in body_copy:
            self.array_fruit_t.append(FRUIT_t(block))

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        self.fruit_cut.reset()
        self.array_fruit_t.clear()
        self.blocks_from_enemy = 0
        # self.__init__(snake_start_speed, snake_change_speed, snake_max_speed)
        # надо подумать тут


        # pygame.quit()
        # sys.exit()

    def draw_grass(self):
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        if self.snake.fast:
            score_text = "Куда летишь? Уже: " + str(self.snake.snack_counter)
            score_x = int(cell_size * cell_number - 100)
            score_y = int(cell_size * cell_number - 40)
        else:
            score_text = str(self.snake.snack_counter)
            score_x = int(cell_size * cell_number - 60)
            score_y = int(cell_size * cell_number - 40)
        score_surface = game_font.render(score_text, True, score_color)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)



