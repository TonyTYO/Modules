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
        h_col: hover colour
        title: title for menu. If None no title band displayed
        title_font: font for title

        use:
        add_item(): to build the menu
        activate(): to show on screen and activate
    """

    __slots__ = ['font', 't_col', 'b_col', 'h_col', 'surface', 'title', 'title_font', 'start_y',
                 '_items', '_b_rects', '_s_rects', '_on_click', '_order', '_hover',
                 'size', 'item_width', 'item_height', 'total_height', 'menu', 'margin', 'position']

    def __init__(self, font=None, t_col=DARK, b_col=WHITE, h_col=D_DARK, title=None, title_font=None):

        if font:                            # Set font for menu items
            self.font = font
        else:
            self.font = pygame.font.SysFont('Tahoma', 18, False, False)
        if title_font:                      # Set font for menu title
            self.title_font = title_font
        else:
            self.title_font = pygame.font.SysFont('Tahoma', 16, False, False)
        self.t_col = t_col          # text colour - default dark grey
        self.b_col = b_col          # background colour - default white
        self.h_col = h_col          # background colour on mouse hover - default light gray
        self.title = title          # Menu title - default None

        self._items = dict()
        self._b_rects = dict()      # Button: button rect
        self._s_rects = dict()      # Button rect on screen
        self._on_click = dict()     # Button: function to execute when button clicked or None
        self._order = dict()        # Button: position in menu
        self._hover = dict()        # True if mouse over button

        self.item_width = 0
        self.item_height = 0
        self.total_height = 0
        self.menu = None
        self.margin, _ = self.font.size("n")
        self.start_y = 0
        self.position = None
        self.surface = None

    @property
    def width(self):
        """ Return width of menu """
        return self.item_width

    @property
    def height(self):
        """ Return height of menu """
        return self.total_height

    @property
    def size(self):
        """ Return size (width, height) of menu """
        return self.item_width, self.total_height

    def add_item(self, no, text, on_click):
        """ Add item to menu
            no: Number of item - items will be shown in this order
            text: Text for item
            on_click: Function to run if item clicked - always sent menu position as parameter
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
        self._draw()

    def activate(self, surface, position):
        """ Draw menu on surface at position
            If item clicked return True
            If mouse clicked off menu return False """
        self.position = position
        self.surface = surface
        self._s_rects = {key: self._update_rect(val, position) for (key, val) in self._b_rects.items()}
        surface.blit(self.menu, position)
        pygame.display.update()
        click_on = self._process_menu()
        return click_on

    def _draw(self):
        """ Draw complete menu on surface self.menu """
        self.total_height = self.item_height * len(self._items)
        t_height, render_title = 0, None
        if self.title:
            render_title = self.title_font.render(self.title, True, self.b_col)
            _, t_height = self.title_font.size(self.title)
            t_height *= 2
            self.total_height += t_height
            self.start_y = t_height
        self.menu = pygame.Surface((self.item_width, self.total_height))
        self.menu.fill(self.b_col)
        if self.title:
            head = pygame.Rect(0, 0, self.item_width, t_height)
            pygame.draw.rect(self.menu, self.t_col, head)
            text_rect = render_title.get_rect(center=(self.item_width // 2, t_height // 2))
            self.menu.blit(render_title, text_rect)
        count = 0
        for no in self._items.keys():
            self._order[no] = count
            self._hover[no] = False
            self._b_rects[no] = pygame.Rect(0, self.start_y + self.item_height * count, self.item_width,
                                            self.item_height)
            self._draw_item(no)
            count += 1

    def _draw_item(self, no):
        """ Draw individual menu item on surface self.menu """
        count = self._order[no]
        border = self._b_rects[no]
        if self._hover[no]:
            pygame.draw.rect(self.menu, self.h_col, border)
        else:
            pygame.draw.rect(self.menu, self.b_col, border)
        pygame.draw.rect(self.menu, self.t_col, border, 1)
        self.menu.blit(self._items[no], (self.margin, self.start_y + self.item_height * count + self.margin))

    @staticmethod
    def _update_rect(rect, pos):
        """ Translate rectangle by pos """
        s_rect = rect.copy()
        s_rect.x += pos[0]
        s_rect.y += pos[1]
        return s_rect

    def _process_menu(self):
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
            else:
                click_on, running = self._process_buttons(event)
                if running:
                    self.surface.blit(self.menu, self.position)
                    pygame.display.update()
        return click_on

    def _button_down(self, mouse):
        """ if mouse clicked on an active button
            Activate button click procedures and return True else False"""
        click_on = False
        if self._items:
            for (but, rect) in self._s_rects.items():
                if rect.collidepoint(mouse):
                    click_on = True
                    self._hover[but] = False
                    self._draw_item(but)
                    if self._on_click[but]:
                        self._on_click[but](self.position)
        return click_on

    def _button_hover(self, mouse):
        """ if mouse above an active button
            Activate button hover procedures """
        if self._items:
            for (but, rect) in self._s_rects.items():
                if rect.collidepoint(mouse):
                    if not self._hover[but]:
                        self._hover[but] = True
                        self._draw_item(but)
                else:
                    if self._hover[but]:
                        self._hover[but] = False
                        self._draw_item(but)

    def _process_buttons(self, event):
        """ Check if mouse interacting with button
            and react accordingly
            click_on: returns True if valid button clicked
            running: returns False if mouse clicked anywhere (used to deactivate menu)"""
        click_on = False
        running = True
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3)[0]:
                running = False
                click_on = self._button_down(mouse)
        else:
            self._button_hover(mouse)
        return click_on, running
