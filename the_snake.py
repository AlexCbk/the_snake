from random import randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Содержит общие атрибуты игрового поля."""

    def __init__(self):
        """Инициализирует базовые атрибуты объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Переопределяется в дочерних классах."""


class Apple(GameObject):
    """Описывает яблоко и действия с ним."""

    def __init__(self, color=APPLE_COLOR):
        """Задает цвет и начальную позицию яблока."""
        super().__init__()
        self.body_color = color
        self.randomize_position(snake_position=self.position)

    def randomize_position(self, snake_position):
        """
        Устанавливает случайную позицию яблока, убедившись, что она
        не совпадает с занятыми позициями змейки.
        """
        while True:
            self.position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )
            if self.position not in snake_position:
                break

    def draw(self):
        """Отрисовывет яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описывает змейку и ее поведение."""

    def __init__(self, color=SNAKE_COLOR):
        super().__init__()
        self.body_color = color
        self.reset()

    def update_direction(self, next_direction=None):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Обновляет позицию змейки (по координатам)."""
        snake_x, snake_y = self.get_head_position()
        dir_x, dir_y = self.direction
        snake_head = (
            ((snake_x + dir_x * GRID_SIZE) + SCREEN_WIDTH) % SCREEN_WIDTH,
            ((snake_y + dir_y * GRID_SIZE) + SCREEN_HEIGHT) % SCREEN_HEIGHT
        )
        self.positions.insert(0, snake_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатие клавиш (движение змейки)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
    return True


def main():
    """Основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        try:
            if not handle_keys(snake):
                break
            snake.update_direction()
            snake.move()
            head_snake = snake.get_head_position()
            if head_snake == apple.position:
                snake.length += 1
                apple.randomize_position(snake.positions)
            if head_snake in snake.positions[1:]:
                screen.fill(BOARD_BACKGROUND_COLOR)
                snake.reset()
            apple.draw()
            snake.draw()
            pygame.display.update()
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            break
    pygame.quit()


if __name__ == '__main__':
    main()
