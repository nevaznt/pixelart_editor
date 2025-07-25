import pygame
import tkinter as tk
from tkinter import filedialog

class Create:
    def __init__(self, window_panel):
        self.window_panel = window_panel
        self.b_new = Button(0, 0, self.window_panel.screen.get_height()*0.06, 'Create New', self.window_panel)
        self.b_new.rect.midright = (self.window_panel.screen.get_width()/2 - 10, self.window_panel.screen.get_height()/2)
        self.b_load = Button(0, 0, self.window_panel.screen.get_height()*0.06, 'Load Image', self.window_panel)
        self.b_load.rect.midleft = (self.window_panel.screen.get_width()/2 + 10, self.window_panel.screen.get_height()/2)

        self.create_panel = pygame.Surface((400, 400))
        self.width = TextField(200, 150, 80, 20, self.window_panel)
        self.width.value = '0'
        self.height = TextField(200, 190, 80, 20, self.window_panel)
        self.height.value = '0'
        self.b_confirm = Button(105, 300, 50, 'Create', self.window_panel)
        self.title_font = pygame.font.Font('JetBrainsMono-Bold.ttf', 40)
        self.font = pygame.font.Font('JetBrainsMono-Bold.ttf', 20)
        self.active_textfield = 'width'

    def update(self):
        mouse_pos = []
        mouse_pos.append(self.window_panel.mouse_pos[0])
        mouse_pos.append(self.window_panel.mouse_pos[1])

        if self.b_new.pressed:
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos[0] -= self.window_panel.screen.get_width()/2 - self.create_panel.get_width()/2
            mouse_pos[1] -= self.window_panel.screen.get_height()/2 - self.create_panel.get_height()/2
            if self.width.update(mouse_pos): self.active_textfield = 'width'
            elif self.height.update(mouse_pos): self.active_textfield = 'height'
            elif mouse_pressed[0]: self.active_textfield = ''

            if self.active_textfield == 'width':
                self.width.active = True
                self.height.active = False
                self.width.register_input()
            elif self.active_textfield == 'height':
                self.width.active = False
                self.height.active = True
                self.height.register_input()
            else:
                self.width.active = False
                self.height.active = False

            self.b_confirm.update(mouse_pos)
            
            if self.b_confirm.pressed and self.width.value[0] != '0' and self.height.value[0] != '0':
                self.window_panel.editing_init(int(self.width.value), int(self.height.value))
            return
        elif self.b_load.pressed:
            
            path = filedialog.askopenfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                title="Choose image (png only)"
            )

            if path == '': 
                self.b_load.pressed = False
            else:
                image = pygame.image.load(path).convert_alpha()
                
                self.window_panel.editing_init(image.get_width(), image.get_height())
                self.window_panel.raster_canvas.pixel_buffer.blit(image, (0, 0))

            return

        self.b_new.update(mouse_pos)
        self.b_load.update(mouse_pos)

    def deactivate_width_textfield(self):
        self.width.active = False

    def deactivate_height_textfield(self):
        self.height.active = False

    def draw(self):
        self.window_panel.screen.fill("#353535")

        if not self.b_new.pressed and not self.b_load.pressed: 
            self.b_new.draw(self.window_panel.screen)
            self.b_load.draw(self.window_panel.screen)

        elif self.b_new.pressed:
            self.create_panel.fill('#353535')

            self.create_panel.blit(self.title_font.render('Canvas Size:', False, '#BFBFBF'), (60, 20))

            self.create_panel.blit(self.font.render('width:', False, '#BFBFBF'), (90, 150))
            self.width.draw(self.create_panel)
            self.create_panel.blit(self.font.render('px', False, '#BFBFBF'), (285, 150))
            self.create_panel.blit(self.font.render('height:', False, '#BFBFBF'), (90, 190))
            self.height.draw(self.create_panel)
            self.create_panel.blit(self.font.render('px', False, '#BFBFBF'), (285, 190))
            
            self.b_confirm.draw(self.create_panel)

            self.window_panel.screen.blit(self.create_panel, (self.window_panel.screen.get_width()/2 - self.create_panel.get_width()/2, self.window_panel.screen.get_height()/2 - self.create_panel.get_height()/2))

class TextField:
    def __init__(self, x, y, width, font_size, window_panel):
        self.active = False
        self.rect = pygame.Rect(x, y, width, font_size*1.5)
        self.value = ''
        self.font = pygame.font.Font('JetBrainsMono-Bold.ttf', font_size)
        self.key_prev = ''
        self.window_panel = window_panel

    def register_input(self):
        keys = pygame.key.get_pressed()
        accepted_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

        if self.active:
            if keys[pygame.K_RETURN] and len(self.value) > 0:
                self.active = False
            elif keys[pygame.K_BACKSPACE] and len(self.value) > 0 and self.key_prev != '<':
                self.value = self.value[:-1]
                self.key_prev = '<'
            elif not keys[pygame.K_BACKSPACE] and self.key_prev == '<':
                self.key_prev = ''
            else:
                for i in range(len(accepted_keys)):
                    if keys[accepted_keys[i]] and str(i) != self.key_prev:
                        self.value += str(i)
                        self.key_prev = str(i)
                    elif not keys[accepted_keys[i]] and str(i) == self.key_prev:
                        self.key_prev = ''

    def update(self, mouse_pos):
        mouse_pressed = pygame.mouse.get_pressed()
        
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]: return True
        else: return False

    def draw(self, surf: pygame.Surface):
        border_color = '#222222'
        if self.active: border_color = pygame.Color(0, 120, 215, 255)
        tmp = pygame.Surface((self.rect.w, self.rect.h))
        text = self.font.render(self.value, True, '#BFBFBF')
        tmp.fill('#303030')
        tmp.blit(text, (2, 0))
        pygame.draw.rect(tmp, border_color, [0, 0, self.rect.w, self.rect.h], 2)
        surf.blit(tmp, self.rect)

class Button:
    def __init__(self, x, y, h, text, window_panel):
        self.rect = pygame.Rect(x, y, (len(text)*h)/1.5, h)
        self.text = text
        self.pressed = False
        self.hover = False
        self.font = pygame.font.Font('JetBrainsMono-Bold.ttf', int(h))
        self.window_panel = window_panel
        self.mouse_prev = pygame.mouse.get_pressed()

    def update(self, mouse_pos):
        mouse_pressed = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):
            self.hover = True
            if self.mouse_prev[0] and not mouse_pressed[0]: self.pressed = True
        else: 
            self.pressed = False
            self.hover = False

        self.mouse_prev = mouse_pressed

    def draw(self, surf: pygame.Surface):
        colors = ('#303030', '#222222', '#A9A9A9')
        if self.hover: colors = ('#222222', "#141414", "#6E6E6E")

        pygame.draw.rect(surf, colors[0], self.rect)
        pygame.draw.rect(surf, colors[1], self.rect, 2)

        text = self.font.render(self.text, False, colors[2])
        surf.blit(text, (self.rect.x + (self.rect.w/2 - text.get_width()/2), self.rect.y + (self.rect.h/2 - text.get_height()/2)))
