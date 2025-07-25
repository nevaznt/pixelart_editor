import pygame

class Palette:
    def __init__(self, window_panel):
        self.active = False
        self.SCREEN_WIDTH = window_panel.screen.get_width()
        self.SCREEN_HEIGHT = window_panel.screen.get_height()
        self.styles = {'width': 250, 'height': 150, 'margin': 5, 'padding': 5, 'border_radius': 15, 'border_width': 1}
        self.position = pygame.Vector2(0, window_panel.screen.get_height() - self.styles['height'] - self.styles['margin']- self.styles['padding'] - 5)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.styles['width'] + self.styles['padding']*2, self.styles['height'] + self.styles['padding']*2)
        self.window_panel = window_panel
        self.palette = []
        for _ in range(10):
            self.palette.append(pygame.Color(0, 0, 0, 0))
        self.palette[0] = pygame.Color(255, 255, 255, 255)
        self.palette[1] = pygame.Color(0, 0, 0, 255)
        self.selected = 0

        self.palette_size = 20
        self.palette_spacing = (((self.styles['width'] + self.styles['padding']*2) / (len(self.palette)/2)) - self.palette_size)/1.5
        self.palette_hitboxes = []
        self.update_palette_hitboxes()

        self.rgba_setting_sliders = [Slider(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 5, 180, self.window_panel, '#FF0000'),
                                     Slider(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 25, 180, self.window_panel, '#00FF00'),
                                     Slider(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 45, 180, self.window_panel, '#0000FF'),
                                     Slider(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 65, 180, self.window_panel, '#000000')]
        self.setup_rgba_settings_sliders()

        self.hex_input = TextField(self.window_panel, self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 80, 70, 15)

    def reset(self):
        self.SCREEN_WIDTH = self.window_panel.screen.get_width()
        self.SCREEN_HEIGHT = self.window_panel.screen.get_height()
        self.position = pygame.Vector2(0, self.window_panel.screen.get_height() - self.styles['height'] - self.styles['margin']- self.styles['padding'] - 5)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.styles['width'] + self.styles['padding']*2, self.styles['height'] + self.styles['padding']*2)
        self.update_palette_hitboxes()
        self.rgba_setting_sliders = [Slider(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 5, 180, self.window_panel, '#FF0000'),
                                     Slider(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 25, 180, self.window_panel, '#00FF00'),
                                     Slider(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 45, 180, self.window_panel, '#0000FF'),
                                     Slider(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 65, 180, self.window_panel, '#000000')]
        self.setup_rgba_settings_sliders()
        self.hex_input.rect.update(self.position.x + self.styles['margin'] + self.styles['padding']*2, self.position.y + self.styles['margin'] + 80, self.hex_input.rect.w, self.hex_input.rect.h)

    def setup_rgba_settings_sliders(self):
        self.rgba_setting_sliders[0].value = self.get_color().r/255
        self.rgba_setting_sliders[1].value = self.get_color().g/255
        self.rgba_setting_sliders[2].value = self.get_color().b/255
        self.rgba_setting_sliders[3].value = self.get_color().a/255

    def update_rgba_settings(self):
        if self.rgba_setting_sliders[0].update(): 
            self.palette[self.selected].r = int(self.rgba_setting_sliders[0].value*255)
        if self.rgba_setting_sliders[1].update(): 
            self.palette[self.selected].g = int(self.rgba_setting_sliders[1].value*255)
        if self.rgba_setting_sliders[2].update(): 
            self.palette[self.selected].b = int(self.rgba_setting_sliders[2].value*255)
        if self.rgba_setting_sliders[3].update(): 
            self.palette[self.selected].a = int(self.rgba_setting_sliders[3].value*255)

    def update_palette_hitboxes(self):
        self.palette_hitboxes = []
        for i in range(int(len(self.palette)/2)):
            self.palette_hitboxes.append(pygame.Rect((self.position.x + self.styles['margin']) + self.styles['padding'] + (self.palette_spacing+self.palette_spacing*i+self.palette_size*i), 
                                                     (self.position.y + self.styles['margin']) + (self.styles['height'] + self.styles['padding']*2)-self.palette_size*2-self.styles['padding']*3, 
                                                     self.palette_size, 
                                                     self.palette_size))
        for i in range(int(len(self.palette)/2), len(self.palette)):
            self.palette_hitboxes.append(pygame.Rect((self.position.x + self.styles['margin']) + self.styles['padding'] + (self.palette_spacing+self.palette_spacing*(i-len(self.palette)/2)+self.palette_size*(i-len(self.palette)/2)), 
                                                     (self.position.y + self.styles['margin']) + (self.styles['height'] + self.styles['padding']*2)-self.palette_size-self.styles['padding'], 
                                                     self.palette_size, 
                                                     self.palette_size))

    def get_color(self):
        return self.palette[self.selected]

    def set_color(self, color: pygame.Color):
        self.palette[self.selected] = color
        self.hex_input.update_color_value()
        self.setup_rgba_settings_sliders()

    def draw_transparency_bg(self, tile_size, surf: pygame.Surface):
        for i in range(0, surf.get_height(), int(tile_size/2)): 
          for j in range(0, surf.get_width(), int(tile_size/2)):
            if i % tile_size == 0 and j % tile_size == 0: pygame.draw.rect(surf,'#8F8F8F', [j, i, tile_size, tile_size])
            elif i % tile_size == 0 and j % tile_size != 0: pygame.draw.rect(surf, '#BFBFBF', [j, i, tile_size, tile_size])
            elif i % tile_size != 0 and j % tile_size != 0: pygame.draw.rect(surf, '#8F8F8F', [j, i, tile_size, tile_size])
            elif i % tile_size != 0 and j % tile_size == 0: pygame.draw.rect(surf, '#BFBFBF', [j, i, tile_size, tile_size])

    def swap_selected_color_with_keys(self):
        key_swaps = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]
        keys = pygame.key.get_pressed()

        for i in range(len(key_swaps)):
            if keys[key_swaps[i]]:
                self.selected = i
                break

    def update(self):
        if self.SCREEN_WIDTH != self.window_panel.screen.get_width() or self.SCREEN_HEIGHT != self.window_panel.screen.get_height():
            self.reset()

        self.swap_selected_color_with_keys()

        mouse_presed = pygame.mouse.get_pressed()

        for i in range(len(self.palette_hitboxes)):
            if self.palette_hitboxes[i].collidepoint(self.window_panel.mouse_pos) and mouse_presed[0]:
                self.selected = i
                self.setup_rgba_settings_sliders()
                self.hex_input.update_color_value()
                self.active = True
                self.window_panel.inter_lock = True
                break
            elif self.active: 
                self.active = False
                self.window_panel.inter_lock = False

        self.update_rgba_settings()

        self.hex_input.update()

    def draw(self):
        width = self.styles['width'] + self.styles['padding']*2
        height = self.styles['height'] + self.styles['padding']*2
        x = self.position.x + self.styles['margin']
        y = self.position.y + self.styles['margin']
        pygame.draw.rect(self.window_panel.screen, '#303030', [x, y, width, height], 0, self.styles['border_radius'])
        pygame.draw.rect(self.window_panel.screen, '#222222', [x, y, width, height], self.styles['border_width'], self.styles['border_radius'])

        color_view_size = 48
        color_view_transparent = pygame.Surface((color_view_size, color_view_size), pygame.SRCALPHA)
        self.draw_transparency_bg(8, color_view_transparent)
        color_view = pygame.Surface((color_view_size, color_view_size), pygame.SRCALPHA)
        color_view_rect = [x + width - color_view_size - self.styles['padding'], y+self.styles['padding'], color_view_size, color_view_size]
        pygame.draw.rect(color_view, self.get_color(), [0, 0, color_view_size, color_view_size])
        pygame.draw.rect(color_view, '#222222', [0, 0, color_view_size, color_view_size], 2)
        color_view_transparent.blit(color_view, (0, 0))
        self.window_panel.screen.blit(color_view_transparent, color_view_rect)

        for i in self.rgba_setting_sliders:
            i.draw()

        for i in range(len(self.palette_hitboxes)):
            palette_view = pygame.Surface((self.palette_hitboxes[i].w, self.palette_hitboxes[i].h), pygame.SRCALPHA)
            pygame.draw.rect(palette_view, self.palette[i], [0, 0, self.palette_hitboxes[i].w, self.palette_hitboxes[i].h], 0)
            border_color = '#222222'
            if i == self.selected: border_color = pygame.Color(0, 120, 215, 255)
            pygame.draw.rect(palette_view, border_color, [0, 0, self.palette_hitboxes[i].w, self.palette_hitboxes[i].h], 2)
            transparency = pygame.Surface((self.palette_hitboxes[i].w, self.palette_hitboxes[i].h), pygame.SRCALPHA)
            self.draw_transparency_bg(8, transparency)
            transparency.blit(palette_view, (0, 0))
            self.window_panel.screen.blit(transparency, self.palette_hitboxes[i])

        self.hex_input.draw()

class Slider:
    def __init__(self, x, y, width, window_panel, color):
        self.window_panel = window_panel
        self.x = x
        self.y = y
        self.width = width
        self.value = 0.0
        self.active = False
        self.color = color
        self.rect = pygame.Rect(x + self.value*width, y, 16, 16)

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()
        return_val = False

        if (self.rect.collidepoint(self.window_panel.mouse_pos) or self.active) and mouse_pressed[0]:
            self.window_panel.inter_lock = True
            self.window_panel.palette.active = True
            self.active = True
            self.value += self.window_panel.mouse_rel[0]/200
            if self.value > 1.0: self.value = 1.0
            elif self.value < 0.0: self.value = 0.0
            self.window_panel.palette.hex_input.update_color_value()
            return_val = True
        elif self.active: 
            self.active = False
            self.window_panel.palette.active = False
            self.window_panel.inter_lock = False

        self.rect = pygame.Rect(self.x + self.value*self.width, self.y, 16, 16)

        return return_val
    def draw(self):
        pygame.draw.line(self.window_panel.screen, '#222222', (self.x, self.y + self.rect.h/2), (self.x + self.width, self.y + self.rect.h/2))

        pygame.draw.rect(self.window_panel.screen, self.color, self.rect, 0, 8)
        pygame.draw.rect(self.window_panel.screen, '#222222', self.rect, 3, 8)

class TextField:
    def __init__(self, window_panel, x, y, width, font_size):
        self.window_panel = window_panel
        self.active = False
        self.value = ''
        self.rect = pygame.Rect(x, y, width, font_size*1.5)
        self.font = pygame.font.Font('C:\\Users\\Chris\\AppData\\Local\\Microsoft\\Windows\\Fonts\\JetBrainsMono-Bold.ttf', font_size)
        self.key_prev = ''

    def update_color_value(self):
        color = self.window_panel.palette.get_color()
        if len(str(hex(color.r))) == 4: r = str(hex(color.r))[2] + str(hex(color.r))[3]
        else: r = str(hex(color.r))[2] + '0'
        if len(str(hex(color.g))) == 4: g = str(hex(color.g))[2] + str(hex(color.g))[3]
        else: g = str(hex(color.r))[2] + '0'
        if len(str(hex(color.b))) == 4: b = str(hex(color.b))[2] + str(hex(color.b))[3]
        else: b = str(hex(color.b))[2] + '0'
        self.value = '#' + r + g + b

    def set_to_palette(self):
        hex_chars = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

        r = hex_chars[self.value[1]] * 16 + hex_chars[self.value[2]]
        g = hex_chars[self.value[3]] * 16 + hex_chars[self.value[4]]
        b = hex_chars[self.value[5]] * 16 + hex_chars[self.value[6]]
        
        self.window_panel.palette.palette[self.window_panel.palette.selected].r = r
        self.window_panel.palette.palette[self.window_panel.palette.selected].g = g
        self.window_panel.palette.palette[self.window_panel.palette.selected].b = b

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        accepted_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, 
                         pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f]
        
        if (self.rect.collidepoint(self.window_panel.mouse_pos) or self.active) and mouse_pressed[0]:
            self.active = True
            self.window_panel.palette.active = True
            self.window_panel.inter_lock = True
        elif keys[pygame.K_RETURN] and len(self.value) == 7:
            self.active = False
            self.window_panel.palette.active = False
            self.window_panel.inter_lock = False
            self.set_to_palette()
        if self.active:
            if keys[pygame.K_BACKSPACE] and len(self.value) > 1 and self.key_prev != '<': 
                self.value = self.value[:-1]
                self.key_prev = '<'
            elif not keys[pygame.K_BACKSPACE] and self.key_prev == '<': 
                self.key_prev = ''
            else:
                for i in range(len(accepted_keys)):
                    if keys[accepted_keys[i]] and len(self.value) < 7 and self.key_prev != str(hex(i))[2]: 
                        self.value += str(hex(i))[2]
                        self.key_prev = str(hex(i))[2]
                        break 
                    elif not keys[accepted_keys[i]] and self.key_prev == str(hex(i))[2]:
                        self.key_prev = ''

    def draw(self):
        border_color = '#222222'
        if self.active: border_color = pygame.Color(0, 120, 215, 255)
        surf = pygame.Surface((self.rect.w, self.rect.h))
        text = self.font.render(self.value, True, '#BFBFBF')
        surf.fill('#303030')
        surf.blit(text, (2, 0))
        pygame.draw.rect(surf, border_color, [0, 0, self.rect.w, self.rect.h], 2)
        self.window_panel.screen.blit(surf, self.rect)
