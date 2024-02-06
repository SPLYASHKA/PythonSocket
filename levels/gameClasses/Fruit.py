from Game_set import *


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, fruit_color, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class FRUIT_t:
    # Временая версия фрукта (не появляется еще раз)
    def __init__(self, pos, team = None):
        self.pos = pos
        self.team = team
        if team == 'blue':
            self.color = blue_snake_fruit_t_color
        elif team == 'red':
            self.color = red_snake_fruit_t_color
        else:
            self.color = fruit_t_color

    def draw_fruit_t(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, self.color, fruit_rect)


class FRUIT_cut:
    def __init__(self):
        self.randomize()
        self.reset()

    def draw_fruit(self):
        if self.fc_check:
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, fruit_cut_color, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def reset(self):
        self.fc_check = False
