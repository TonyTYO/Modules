# -------------------------------------------------------------------------------
# Name:        dialogue
# Purpose:     Handles dialogue boxes in pygame
# Author:      Tony
# Created:     25/08/2016
# Copyright:   (c) Tony 2016
# Licence:     Free to use
# -------------------------------------------------------------------------------

# ! /usr/bin/env python

""" Sets up dialogue box on screen
    Dependencies : pygame, textbox, pygbuttons
"""

import sys
import pygame
from pygame.locals import *
import textbox as tbox
import pygbuttons

LIGHTSLATEGRAY = (119, 136, 153)
DARK = (100, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class DialogueException(Exception):
    """ Class that raises an exception if error found while printing string """

    __slots__ = ['message', 'line', 'extra_msg']

    def __init__(self, message=None, line="", extra_msg=""):
        super(DialogueException, self).__init__(message)
        self.message = message
        self.line = line
        self.extra_msg = extra_msg
        sys.tracebacklimit = 0


class Dialogue(tbox.Textwrap):
    """ Class to show dialogue on screen 
        Can be any number of buttons, specified in a dictionary
        waits for button to be clicked and returns the text on the button clicked
        returns None if window closed """
    __slots__ = ['screen', 'rect', 'background_colour', 'surface', 'buttons', 'active_buttons', 'image', 'result']

    def __init__(self, screen, rect, font=None, text_colour=BLACK,
                 background_colour=WHITE, justification=21, frame=4, frame_colour=DARK):
        """ Create the text box inside which text will be printed
            screen: surface to be blitted on - required
            rect:   rectangle to contain the writing - required
            font:   default font for text - required
            text_color: default colour for text
            background_color: colour of box background
            justification:  0(default)-left, 1-centred, 2-right.
                            add 10 for vertical centred
                            add 20 for vertical centred with room for dialogue buttons
            frame: 0(default)-no frame, otherwise thickness of frame
            frame_colour: Black(default) otherwise RGB colour triple
        """
        if not font:
            font = pygame.font.SysFont('Tahoma', 24, False, False)
        tbox.Textwrap.__init__(self, screen, rect, font, text_colour,
                               background_colour, justification, frame, frame_colour)
        self.screen = screen
        self.rect = rect
        self.background_colour = background_colour
        self.surface = None
        self.buttons = None
        self.active_buttons = None
        self.image = pygame.Surface(self.rect.size)
        self.result = None

    def show_dialogue(self, msg, bwtwm, width=140, height=40, spacing=10):
        """ Show dialogue on screen and wait for user choice
            bwtwm: dictionary specifying buttons {no: text} eg {1: "yes", 2: "no"}
            width, height: width and height of buttons
            spacing: space between buttons """

        keys = list(bwtwm.keys())
        if min(keys) != 1:
            raise DialogueException("Button numbers in dictionary must start with number 1")
        if len(keys) != max(keys):
            raise DialogueException("Button numbers in dictionary must be consecutive")

        background = pygame.Surface(self.rect.size)
        bg = self.screen.subsurface(self.rect)
        background.blit(bg, (0, 0))
        self.surface = self.print_text(msg)
        self.buttons = pygbuttons.Buttons()

        surface_w, surface_h = self.surface.get_size()
        button_w, button_h, button_s = width, height, spacing
        buttons_y = surface_h - button_h - 15 + self.rect.y

        no = len(bwtwm)
        if no % 2 == 0:
            leftmost_x = self.rect.x + surface_w // 2 - button_w - button_s // 2 - (no - 2) // 2 * (button_w + button_s)
        else:
            leftmost_x = self.rect.x + surface_w // 2 - (button_w // 2) - no // 2 * (button_w + button_s)
        if leftmost_x < 0:
            raise DialogueException("Buttons off screen: Reduce sizes and spacing or increase Dialogue size")
        b_pos = [leftmost_x]
        for i in range(1, no):
            b_pos.append(leftmost_x + i * (button_w + button_s))

        # This formula combines the two above to give the leftmost x for any number of buttons
        # leftmost_x = self.rect.x + surface_w // 2 - (
        #     button_w // 2 + no // 2 * (button_w + 10) if no % 2 != 0 else no / 2 * (button_w + 10) - 5)

        # Assign loop variable to variable in lambda scope
        # Otherwise all lambdas will have last loop value of text
        for butt, text in bwtwm.items():
            button = pygbuttons.Button(self.screen)
            button.set_button(text, x=b_pos[butt - 1], y=buttons_y, w=button_w, h=button_h)
            self.buttons.add_button(button, text)
            self.buttons.add_click(button, lambda n=text: self._get_new(n))
            self.buttons.add_hover(button)
            self.buttons.set_active(button, True)
            self.buttons.set_visible(button, True)

        self.screen.blit(self.surface, self.rect.topleft)
        pygame.display.update()

        """ main loop """
        running = True

        while running:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    running = False
            elif event.type == QUIT:
                running = False

            self.buttons.process_buttons(event)
            if self.result:
                running = False

            pygame.display.update()

        self.screen.blit(background, self.rect)
        pygame.display.update(self.rect)
        return self.result

    def _get_new(self, name):
        self.result = name
