# -------------------------------------------------------------------------------
# Name:        menu
# Purpose:     Create and use a menu in pygame
# Author:      Tony
# Created:     25/08/2016
# Copyright:   (c) Tony 2016
# Licence:     Free to use
# -------------------------------------------------------------------------------

# ! /usr/bin/env python

""" Create and use a menu in pygame
    Dependencies : pygame
"""
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT = (170, 170, 170)
DARK = (100, 100, 100)
D_LIGHT = (220, 220, 220)
D_DARK = (192, 192, 192)
MAGENTA = (255, 0, 255)


class Menu:
    """ Allows menu to be created and activated in pygame
        font: font for text
        t_col: text colour
        b_col: background colour
    """

    __slots__ = ['font', 't_col', 'b_col', '_items', '_b_rects', '_s_rects', '_on_click',
                 'size', 'item_width', 'item_height', 'total_height', 'menu', 'margin', 'position']

    def __init__(self, font=None, t_col=DARK, b_col=WHITE):

        if font:
            self.font = font
        else:
            self.font = pygame.font.SysFont('Tahoma', 18, False, False)
        self.t_col = t_col
        self.b_col = b_col

        self._items = dict()
        self._b_rects = dict()  # Button: button rect
        self._s_rects = dict()  # Button rect on screen
        self._on_click = dict()  # Button: function to execute when button clicked or None
        self.size = dict()
        self.item_width = 0
        self.item_height = 0
        self.total_height = 0
        self.menu = None
        self.margin, _ = self.font.size("n")
        self.position = None

    @property
    def width(self):
        """ Return width of menu """
        return self.item_width

    @property
    def height(self):
        """ Return height of menu """
        return self.total_height

    def get_size(self):
        """ Return size (width, height) of menu """
        return self.item_width, self.total_height

    def add_item(self, no, text, on_click):
        """ Add item to menu
            no: Number of item
            text: Text for item
            on_click: Function to run if item clicked
        """
        render_text = self.font.render(text, True, self.t_col)
        text_width, text_height = self.font.size(text)
        width, height = text_width + 2 * self.margin, text_height + 2 * self.margin
        if self.item_width < width:
            self.item_width = width
        if self.item_height < height:
            self.item_height = height
        self._items[no] = render_text
        self._on_click[no] = on_click
        self.total_height = self.item_height * len(self._items)
        self.draw()

    def draw(self):
        """ Draw menu on surface self.menu """
        self.total_height = self.item_height * len(self._items)
        self.menu = pygame.Surface((self.item_width, self.total_height))
        self.menu.fill(self.b_col)
        count = 0
        for no in self._items.keys():
            border = pygame.Rect(0, self.item_height * count, self.item_width, self.item_height)
            pygame.draw.rect(self.menu, self.t_col, border, 1)
            self._b_rects[no] = border
            self.menu.blit(self._items[no], (self.margin, self.item_height * count + self.margin))
            count += 1

    def activate(self, surface, position):
        """ Draw menu on surface at position """
        self.position = position
        self._s_rects = {key: self.update_rect(val, position) for (key, val) in self._b_rects.items()}
        surface.blit(self.menu, position)
        pygame.display.update()

    @staticmethod
    def update_rect(rect, pos):
        """ Translate rectangle by pos """
        s_rect = rect.copy()
        s_rect.x += pos[0]
        s_rect.y += pos[1]
        return s_rect

    def process_menu(self):
        """ Process menu
            if item clicked run on_click function and return True
            if mouse clicked off menu return False
        """
        running = True
        click_on = False
        while running:
            pygame.event.pump()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                click_on = False
                if self._items:
                    for (but, rect) in self._s_rects.items():
                        if rect.collidepoint(pos):
                            click_on = True
                            if self._on_click[but]:
                                self._on_click[but](self.position)

        return click_on
