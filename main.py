import pygame
import random
import sys
from time import sleep
from Py_files.bottle import Bottle
from Py_files.settings import *

pygame.init()
background = pygame.image.load("Images/background.jpg")
size = width_screen, height_screen = 1000, 750
screen = pygame.display.set_mode(size)
icon_surface = pygame.image.load("Images/icon.png")
pygame.display.set_icon(icon_surface)
pygame.display.set_caption("Color Sort Bottles")
clock = pygame.time.Clock()
color_names = list(colors_rgb.keys())
first_pick = None
second_pick = None


def create_bottles(level):
    """ Начало уровня:
     1) создание атрибута в виде списка, в котором хранится level + 3 бутылок и информауия о них (жидкости, их позиции)
     2) жидкости рандомно перемешиваются """
    amount_of_bottles = level + 3
    Bottle.bottles = []
    random_colors = random.sample(color_names, amount_of_bottles - 1)
    liquids = (random_colors * 20)[:amount_of_bottles*4]
    random.shuffle(liquids)
    for i in range(amount_of_bottles):
        bottle_position = x, y = (width_screen // (amount_of_bottles + 1)) * i + \
                                 (width_screen - amount_of_bottles * 80) // (amount_of_bottles + 1), 120
        # Позиции жидкостей в бутылке. Всегда по 4 жидкости в бутылке в начале игры
        liquid_positions = [
            (x, y + bottle_size[1] - 224),
            (x, y + bottle_size[1] - 168),
            (x, y + bottle_size[1] - 112),
            (x, y + bottle_size[1] - 56)
        ]
        Bottle(
            screen,
            bottle_position,
            liquids=liquids[i*4:i*4+4],
            liquid_positions=liquid_positions
        )


def win() -> bool:
    """ Проверка на то, отсортированы ли все цвета в бутылках"""
    # Проверка: нет ли бутылок с одним цветом
    first_colors_bottles = [i.liquids[0] if len(i.liquids) > 0 else None for i in Bottle.bottles]
    if len(first_colors_bottles) != len(set(first_colors_bottles)):
        return False
    # Проверка на то, что в бутылках один цвет
    for i in Bottle.bottles:
        if len(set(i.liquids)) > 1:
            return False
    return True


def start_level(level):
    global first_pick, second_pick
    create_bottles(level)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for jar in Bottle.bottles:
                    if jar.bottle.collidepoint(e.pos):
                        if first_pick:  # Если бутылка уже была выбрана, и это уже второе нажатие
                            second_pick = jar
                            first_pick.move_top(second_pick)
                            first_pick, second_pick = None, None
                        else:  # Иначе сохраняем выбранную в первый раз бутылку
                            jar.picked = True
                            first_pick = jar
        screen.blit(background, (0, 0))
        # Рисуем бутылки
        for bottle in Bottle.bottles:
            bottle.draw()
        # Проверка на то, отмортированы жидкости или нет
        if win():
            pygame.display.flip()
            sleep(1)
            create_bottles(level)
        pygame.display.flip()


# Класс, реализующий рисование прямоугольной кнопки
class Button:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

    def draw_button(self, x, y, text, font_size=40, key=None, **kwargs):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.color, (x, y, self.width, self.height))
            if click[0]:
                pygame.time.delay(300)
                if kwargs is not None:
                    key(**kwargs)
                else:
                    key()
        else:
            pygame.draw.rect(screen, self.color, (x, y, self.width, self.height))
        print_text(text, (x + 5, y + 10), (0, 102, 0), font_size)


def print_text(text, position, font_color, font_size):
    font_type = pygame.font.Font(None, font_size)
    text = font_type.render(text, True, font_color)
    screen.blit(text, position)


def show_levels():
    screen.blit(background, (0, 0))
    print_text("ВЫБЕРИТЕ УРОВЕНЬ ИГРЫ!", (100, 150), main_head_color, 80)
    level_1 = Button(175, 45, (217, 217, 196))
    level_2 = Button(175, 45, (217, 217, 196))
    level_3 = Button(175, 45, (217, 217, 196))
    level_4 = Button(175, 45, (217, 217, 196))
    level_5 = Button(175, 45, (217, 217, 196))
    back = Button(100, 45, (217, 217, 196))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        level_1.draw_button(385, 270, "УРОВЕНЬ 1", key=start_level, level=1)
        level_2.draw_button(385, 340, "УРОВЕНЬ 2", key=start_level, level=2)
        level_3.draw_button(385, 410, "УРОВЕНЬ 3", key=start_level, level=3)
        level_4.draw_button(385, 480, "УРОВЕНЬ 4", key=start_level, level=4)
        level_5.draw_button(385, 550, "УРОВЕНЬ 5", key=start_level, level=5)
        back.draw_button(423, 620, "Назад", key=start_screen)
        pygame.display.flip()
        clock.tick(15)


def show_menu():
    button_start = Button(205, 45, (217, 217, 196))
    button_information = Button(150, 45, (217, 217, 196))
    button_quit = Button(120, 45, (217, 217, 196))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        button_start.draw_button(385, 410, "НАЧАТЬ ИГРУ", key=show_levels)
        button_information.draw_button(412, 480, "ПРАВИЛА")
        button_quit.draw_button(425, 550, "ВЫХОД", key=sys.exit)
        pygame.display.flip()
        clock.tick(15)


def start_screen():
    screen.blit(background, (0, 0))
    print_text("Get Color", (290, 150), main_head_color, 130)
    show_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


start_screen()
