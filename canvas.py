import pygame

class Raster_canvas:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.pixel_buffer = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.preview_buffer = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.position = pygame.Vector2(0, 0)
        self.zoom = 1
        self.transparency_bg = pygame.Surface((0, 0))

    def set_position_center(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.position.x = SCREEN_WIDTH/2
        self.position.y = SCREEN_HEIGHT/2

    def zoomin(self, num):
        self.zoom += num

    def update_transparency_bg(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.transparency_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        scale = 16
        for i in range(0, self.transparency_bg.get_height(), int(scale/2)): 
          for j in range(0, self.transparency_bg.get_width(), int(scale/2)):
              if i % scale == 0 and j % scale == 0: pygame.draw.rect(self.transparency_bg,'#8F8F8F', [j, i, scale, scale])
              elif i % scale == 0 and j % scale != 0: pygame.draw.rect(self.transparency_bg, '#BFBFBF', [j, i, scale, scale])
              elif i % scale != 0 and j % scale != 0: pygame.draw.rect(self.transparency_bg, '#8F8F8F', [j, i, scale, scale])
              elif i % scale != 0 and j % scale == 0: pygame.draw.rect(self.transparency_bg, '#BFBFBF', [j, i, scale, scale])

    def get_position_topleft(self):
        return self.position.x - (self.WIDTH*self.zoom)/2, self.position.y - (self.HEIGHT*self.zoom)/2

    def get_zoomed_size(self):
        return self.WIDTH * self.zoom, self.HEIGHT * self.zoom

    def scroll_zoom(self, window_panel):
        if window_panel.mousewheel > 0: self.zoomin(window_panel.mousewheel)
        elif window_panel.mousewheel < 0: self.zoomin(window_panel.mousewheel)

    def blit_preview(self):
        self.pixel_buffer.blit(self.preview_buffer, (0, 0))

    def canvas_movement(self, window_panel):
        mouse_pressed = pygame.mouse.get_pressed()
        
        if mouse_pressed[1]: 
            self.position.x += window_panel.mouse_rel[0]
            self.position.y += window_panel.mouse_rel[1]

    def update(self, window_panel):
        self.scroll_zoom(window_panel)
        self.canvas_movement(window_panel)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_t]: 
            self.set_position_center(window_panel.screen.get_width(), window_panel.screen.get_height())
            window_panel.tool_set.position.x = 0
            window_panel.tool_set.position.y = 0

    def draw(self, surf: pygame.Surface, SCREEN_WIDTH, SCREEN_HEIGHT):
        canvas_x, canvas_y = self.get_position_topleft()
        canvas_w, canvas_h = self.get_zoomed_size()

        scaled_canvas = pygame.transform.scale(self.pixel_buffer, (canvas_w, canvas_h))
        scaled_preview = pygame.transform.scale(self.preview_buffer, (canvas_w, canvas_h))

        if self.transparency_bg.get_width() != SCREEN_WIDTH or self.transparency_bg.get_height() != SCREEN_HEIGHT:
           self.update_transparency_bg(SCREEN_WIDTH, SCREEN_HEIGHT)

        tmp = pygame.Surface((canvas_w, canvas_h))
        tmp.blit(self.transparency_bg, (-canvas_x, -canvas_y))
        tmp.blit(scaled_canvas, (0, 0))
        tmp.blit(scaled_preview, (0, 0))

        surf.blit(tmp, (canvas_x, canvas_y))

        #borber
        border_width = 1
        pygame.draw.rect(surf, "#A9A9A9", [canvas_x-border_width, canvas_y-border_width, canvas_w+border_width*2, canvas_h+border_width*2], border_width)