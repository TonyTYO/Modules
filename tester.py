# Author:      Tony
#
# Created:     04/07/2016
# Copyright:   (c) Tony 2016
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import pygame
import textbox as tbox
import userinput as ui
import dialogue as di


def m1():
    wordfile = None
    try:
        wordfile = open(r"res\sowpods.txt", 'r')  # list of allowed scrabble words
    except IOError as e:
        print(e)
    wordsread = wordfile.readlines()  # read into list
    words = [i.strip() for i in wordsread]  # remove white space
    for w in words:
        if len(w) == 5 and w[0] == "u" and w[-1] == "n":
            print(w)


def main():
    pygame.init()
    pygame.font.init()

    tboxtest()
    uitest()
    dialtest()
    pygame.quit()


def tboxtest():
    display = pygame.display.set_mode((800, 600))
    display.fill((119, 136, 153))
    my_rect = pygame.Rect((40, 40, 400, 500))
    i_font = pygame.font.SysFont("arialms", 36)

    tw = tbox.Textwrap(display, my_rect, i_font, (190, 190, 190), (255, 255, 255), 11, 10, (255, 0, 0))
    tw.print_text(
        "This is a test of a very long line including \Bbold formatting\B and \C(255, 0, 0)coloured text\C. \SMore to "
        "come\S. \I\BBold and Italic!\B\I AND \F(comicsansms, 32)\B\C(0, 0, 255)How about this\C\B\F weird! no\n")

    pygame.display.update()

    while not pygame.event.wait().type in (pygame.QUIT, pygame.KEYDOWN):
        pass


def uitest():
    display = pygame.display.set_mode((800, 600))
    display.fill((211, 211, 211))
    i_font = pygame.font.SysFont("arialms", 20)

    user = ui.Uinput(display, pygame.Rect([40, 100, 200, 40]), i_font, 20, frame=4)
    name1 = user.get_input(10, default="one")

    pygame.display.update()

    while not pygame.event.wait().type in (pygame.QUIT, pygame.KEYDOWN):
        pass


def dialtest():
    display = pygame.display.set_mode((800, 600))
    display.fill((119, 136, 153))
    my_rect = pygame.Rect((40, 40, 600, 300))
    i_font = pygame.font.SysFont("arial", 20)

    dia = di.Dialogue(display, my_rect)
    # result = dia.show_dialogue("Do you want to end game?", "yes/no")
    # dia.show_dialogue("Do you want to end game?", "continue")
    result = dia.show_dialogue("Do you want to end game?", {1: "yes", 2: "no", 3: "cancel", 4: "quit"}, 100, 40, 2)
    # result = dia.show_dialogue("Do you want to end game?", {1:"yes", 2:"no", 3:"cancel"})
    # result = dia.show_dialogue("Do you want to end game?", {1: "yes", 2: "no"})
    # result = dia.show_dialogue("Do you want to end game?", {1: "cancel"})
    print(result)
    if result in ['no', 'continue']:
        tboxtest()

    pygame.display.update()

    while not pygame.event.wait().type in (pygame.QUIT, pygame.KEYDOWN):
        pass


if __name__ == '__main__':
    main()
