import pygame
from random import randrange

RES = 800  # размер рабочего окна
SIZE = 50  # размер секций змейки
WHITE = (255, 255, 255)  # цвет фона
RED = (255, 0, 0)  # цвет яблока
GREEN = (0, 255, 0)  # цвет змейки


class SnakeGame:
    def __init__(self):
        self.snake = [(randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE))]  # начальная позиция змейки
        self.apple = (randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE))  # начальная позиция яблока
        self.direction = 'RIGHT'  # начальное направление движения змейки
        self.change_to = self.direction  # переменная для изменения направления
        self.score = 0  # начальное количество очков

        pygame.init()  # инициализация Pygame
        self.win = pygame.display.set_mode((RES, RES))  # создание окна игры
        pygame.display.set_caption('Змейка')  # заголовок окна
        self.clock = pygame.time.Clock()  # объект для управления временем в игре

    def run(self):
        self.playing = True  # флаг для состояния игры (игра продолжается)
        while self.playing:
            self._handle_events()  # обработка событий (например, нажатия клавиш)
            self._change_direction()  # изменение направления движения змейки
            self._move()  # перемещение змейки
            self._check_collision()  # проверка на столкновения
            self._update_screen()  # обновление экрана
            self.clock.tick(5)  # установка скорости

        self.game_over()  # вызов функции для вывода сообщения о проигрыше

    def _handle_events(self): #проверка нажатий на клавиши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если пользователь закрывает окно
                self.playing = False  # игра завершается
            elif event.type == pygame.KEYDOWN:  # если пользователь нажимает клавишу
                if event.key == pygame.K_LEFT:
                    self.change_to = 'LEFT'  # изменяем направление налево
                elif event.key == pygame.K_RIGHT:
                    self.change_to = 'RIGHT'  # изменяем направление направо
                elif event.key == pygame.K_UP:
                    self.change_to = 'UP'  # изменяем направление вверх
                elif event.key == pygame.K_DOWN:
                    self.change_to = 'DOWN'  # изменяем направление вниз

    def _change_direction(self):
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':  # если пользователь выбрал лево и змейка не движется вправо
            self.direction = 'LEFT'  # змейка начинает двигаться влево
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':  # если пользователь выбрал право и змейка не движется влево
            self.direction = 'RIGHT'  # змейка начинает двигаться вправо
        if self.change_to == 'UP' and self.direction != 'DOWN':  # если пользователь выбрал вверх и змейка не движется вниз
            self.direction = 'UP'  # змейка начинает двигаться вверх
        if self.change_to == 'DOWN' and self.direction != 'UP':  # если пользователь выбрал вниз и змейка не движется вверх
            self.direction = 'DOWN'  # змейка начинает двигаться вниз

    def _move(self):  # направление движения
        x, y = self.snake[0]  # текущие координаты головы змейки
        if self.direction == 'LEFT':
            x -= SIZE  # движение влево
        if self.direction == 'RIGHT':
            x += SIZE  # движение вправо
        if self.direction == 'UP':
            y -= SIZE  # движение вверх
        if self.direction == 'DOWN':
            y += SIZE  # движение вниз

        # Змейка проходит сквозь левую и правую стены
        x = x % RES

        # Проверка на проигрыш (столкновение с верхней или нижней границей)
        if y < 0 or y >= RES:
            self.playing = False  # если змейка вышла за границы, игра заканчивается

        self.snake.insert(0, (x, y))  # добавляем новую голову змейки

    def _check_collision(self): # рост змейки
        if self.snake[0] == self.apple:  # если змейка съела яблоко
            self.score += 1  # увеличиваем счет
            self.apple = (randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE))  # создаем новое яблоко
        else:
            self.snake.pop()  # удаляем последний сегмент змейки (она не растет)

        # проверка столкновения с самим собой
        if len(self.snake) != len(set(self.snake)):
            self.playing = False  # если змейка столкнулась с самой собой, игра заканчивается

    def _update_screen(self):  # вид на экране
        self.win.fill(WHITE)  # цвет экрана
        for i in self.snake:
            pygame.draw.rect(self.win, GREEN, (*i, SIZE, SIZE))  # рисуем змейку
        pygame.draw.rect(self.win, RED, (*self.apple, SIZE, SIZE))  # рисуем яблоко
        self.show_score()  # отображаем текущий счет
        pygame.display.update()  # обновляем экран

    def game_over(self): # экран при проигрыше
        font = pygame.font.SysFont(None, 100)  # шрифт и размер текста
        text = font.render('ПОТРАЧЕНО', True, RED)  # создаем текст "ПОТРАЧЕНО" красного цвета
        text_rect = text.get_rect(center=(RES // 2, RES // 2))  # задаем положение текста по центру экрана
        self.win.blit(text, text_rect)  # отображаем текст на экране
        pygame.display.update()  # обновляем экран

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # закрываем окно при нажатии на крестик
                    return

    def show_score(self): # отображение счета
        font = pygame.font.SysFont(None, 36)  # выбираем шрифт и размер текста
        score_text = font.render(f'Score: {self.score}', True, GREEN)  # создаем текст с текущим счетом зеленого цвета
        self.win.blit(score_text, (10, 10))  # отображаем текст на экране


game = SnakeGame()  # создаем объект игры
game.run()  # запускаем игру

pygame.quit()  # закрываем Pygame при выходе из игры