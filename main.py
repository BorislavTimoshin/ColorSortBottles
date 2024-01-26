import pygame
import random
from time import sleep
from Py_files.bottle import Bottle
from Py_files.settings import colors_rgb, bottle_size

running = True
background = pygame.image.load("Images/background.jpg")
size = width, height = 1000, 750
screen = pygame.display.set_mode(size)
icon_surface = pygame.image.load("Images/icon.png")
pygame.display.set_icon(icon_surface)
pygame.display.set_caption("Color Sort Bottles")

color_names = list(colors_rgb.keys())
first_pick = None
second_pick = None


def start_level(level):
    """ Начало уровня:
     1) создание атрибута в виде списка, в котором хранятся бутылки и информауия о них (жидкости, позиции жидкостей)
     2) жидкости рандомно перемешиваются """
    Bottle.bottles = []
    random_colors = random.sample(color_names, level - 1)
    liquids = (random_colors * 20)[:level*4]
    random.shuffle(liquids)
    for i in range(level):
        bottle_position = x, y = (width // (level + 1)) * i + (width - level * 80) // (level + 1), 120
        # Позиции жидкостей в бутылке
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
    # Проверка на то, что нет бутылок с одним цветом
    first_colors_bottles = [i.liquids[0] if len(i.liquids) > 0 else None for i in Bottle.bottles]
    if len(first_colors_bottles) != len(set(first_colors_bottles)):
        return False
    # Проверка на то, что в бутылках один цвет
    for i in Bottle.bottles:
        if len(set(i.liquids)) > 1:
            return False
    return True


start_level(4)

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            for jar in Bottle.bottles:
                if jar.bottle.collidepoint(e.pos):
                    if first_pick:
                        second_pick = jar
                        first_pick.move_top(second_pick)
                        first_pick, second_pick = None, None
                    else:
                        jar.picked = True
                        first_pick = jar

    screen.blit(background, (0, 0))

    for bottle in Bottle.bottles:
        bottle.draw()

    if win():
        pygame.display.flip()
        sleep(1)
        start_level(5)

    pygame.display.flip()
