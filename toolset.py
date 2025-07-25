import math
import pygame

class Tool_set:
    def __init__(self, window_panel):
        self.active = False
        self.position = pygame.Vector2(0, 0)
        self.window_panel = window_panel
        self.tools = [Pencil(window_panel), Eraser(window_panel), Picker(window_panel), Fill(window_panel), Shape(window_panel), Shape(window_panel, 1)]
        self.move = Move_Tool_set(window_panel)
        self.selected = 0
        self.styles = {'margin': 5, 'padding': 5, 'border_radius': 15, 'icon_width': 48, 'icon_height': 48, 'border_width': 1}
        self.hitboxes = []
        self.update_hitboxes()
        self.prev_mouse_pressed = pygame.mouse.get_pos()

        return

    def update_hitboxes(self):
        self.hitboxes = []
        for i in range(len(self.tools)):
            self.hitboxes.append(pygame.Rect(self.position.x + self.styles['margin']+self.styles['padding'], 
                                             self.position.y + self.styles['margin']+self.styles['padding']+i*self.styles['icon_height'], 
                                             self.tools[i].icon.get_width(), 
                                             self.tools[i].icon.get_height()))
        self.move.hitbox = pygame.Rect(self.position.x + self.styles['margin']+self.styles['padding'], self.position.y + self.styles['margin']+self.styles['padding'] + len(self.tools)*self.styles['icon_height'], self.move.icon.get_width(), self.move.icon.get_height())

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        for i in range(len(self.hitboxes)):
            if self.hitboxes[i].collidepoint(mouse_pos) and mouse_pressed[0] and not self.move.active: 
                self.active = True
                self.window_panel.inter_lock = True
                if not self.prev_mouse_pressed[0]: 
                    if self.selected == i and type(self.tools[self.selected]) == Shape:
                        self.tools[self.selected].nextShape()
                    self.selected = i
                break
            elif self.active:
                self.active = False
                self.window_panel.inter_lock = False

        if keys[pygame.K_p]: self.selected = 0
        elif keys[pygame.K_e]: self.selected = 1
        elif keys[pygame.K_f]: self.selected = 2
        elif keys[pygame.K_c]: self.selected = 3
        elif keys[pygame.K_s]: self.selected = 4
        elif keys[pygame.K_o]: self.selected = 5

        self.move.update()
        self.update_hitboxes()
        if not self.window_panel.palette.rect.collidepoint(self.window_panel.mouse_pos): self.tools[self.selected].update()

        self.prev_mouse_pressed = mouse_pressed

    def draw(self):
        toolset_rect = [self.position.x + self.styles['margin'], self.position.y + self.styles['margin'], self.styles['icon_width']+self.styles['padding']*2, (len(self.tools)*self.styles['icon_height']+self.styles['padding']*2) + self.move.icon.get_height()]
        pygame.draw.rect(self.window_panel.screen, '#303030', toolset_rect, 0, self.styles['border_radius'])
        pygame.draw.rect(self.window_panel.screen, '#222222', toolset_rect, self.styles['border_width'], self.styles['border_radius'])

        for i in range(len(self.tools)):
            self.window_panel.screen.blit(self.tools[i].icon, (self.position.x + self.styles['margin']+self.styles['padding'], self.position.y + self.styles['margin']+self.styles['padding']+(i*self.styles['icon_height'])))
            if i == self.selected:
                tmp = pygame.Surface((self.tools[i].icon.get_width(), self.tools[i].icon.get_height()), pygame.SRCALPHA)
                pygame.draw.rect(tmp, pygame.Color(0, 120, 215, 40), [0, 0, tmp.get_width(), tmp.get_height()], 0, 10)
                pygame.draw.rect(tmp, pygame.Color(0, 120, 215, 255), [0, 0, tmp.get_width(), tmp.get_height()], 1, 10)
                self.window_panel.screen.blit(tmp, (self.position.x + self.styles['margin']+self.styles['padding'], self.position.y + self.styles['margin']+self.styles['padding']+(i*self.styles['icon_height'])))

            if i == len(self.tools)-1:
                self.window_panel.screen.blit(self.move.icon, (self.position.x + self.styles['margin']+self.styles['padding'], self.position.y + self.styles['margin']+self.styles['padding']+(i*self.styles['icon_height']) + self.styles['icon_height']))
        
        for i in range(len(self.tools)):
            if i == self.selected:
                self.window_panel.screen.blit(pygame.transform.scale(self.tools[i].icon, (self.tools[i].icon.get_width()/2, self.tools[i].icon.get_height()/2)), (self.window_panel.mouse_pos[0], self.window_panel.mouse_pos[1]-self.tools[i].icon.get_height()/2))

        self.tools[self.selected].draw()

class Tool:
    def __init__(self, window_panel, icon):
        self.window_panel = window_panel
        self.icon = icon
        self.holding_mouse = False
        self.active = False

    def get_mouse_canvas_coordinates(self, mouse_pos, canvas_x, canvas_y):
        return int((mouse_pos[0]-canvas_x)/self.window_panel.raster_canvas.zoom), int((mouse_pos[1]-canvas_y)/self.window_panel.raster_canvas.zoom)

    def is_in_canvas_space(self, mouse_pos, canvas_x, canvas_y, canvas_w, canvas_h) -> bool:
        return canvas_x < mouse_pos[0]+1 and canvas_x + canvas_w > mouse_pos[0] and canvas_y < mouse_pos[1]+1 and canvas_y + canvas_h > mouse_pos[1]

class Move_Tool_set(Tool):
    def __init__(self, window_panel):
        Tool.__init__(self, window_panel, pygame.image.load('icons/move_toolset_tool_icon.png'))
        self.hitbox = pygame.Rect(0, 0, 0 ,0)

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0]:
            if self.hitbox.collidepoint(self.window_panel.mouse_pos) or self.active:
                self.window_panel.tool_set.active = True
                self.window_panel.inter_lock = True
                self.active = True
                self.window_panel.tool_set.position.x += self.window_panel.mouse_rel[0]
                self.window_panel.tool_set.position.y += self.window_panel.mouse_rel[1]
        elif self.active: 
            self.active = False
            self.window_panel.tool_set.active = False
            self.window_panel.inter_lock = False

    def draw(self):
        pass

class Pencil(Tool):
    def __init__(self, window_panel):
        Tool.__init__(self, window_panel, pygame.image.load('icons/pencil_tool_icon.png'))

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()

        canvas_x, canvas_y = self.window_panel.raster_canvas.get_position_topleft()
        canvas_w, canvas_h = self.window_panel.raster_canvas.get_zoomed_size()

        if self.is_in_canvas_space(self.window_panel.mouse_pos, canvas_x, canvas_y, canvas_w, canvas_h) and not self.window_panel.tool_set.active:
            if mouse_pressed[0]:
                self.active = True
                self.window_panel.tool_set.active = True
                self.window_panel.inter_lock = True
                mouse_canvas_x, mouse_canvas_y = self.get_mouse_canvas_coordinates(self.window_panel.mouse_pos, canvas_x, canvas_y)
                self.window_panel.raster_canvas.pixel_buffer.set_at((mouse_canvas_x, mouse_canvas_y), self.window_panel.palette.get_color())
            elif self.active: 
                self.active = False
                self.window_panel.tool_set.active = False
                self.window_panel.inter_lock = False

    def draw(self):
        pass

class Eraser(Tool):
    def __init__(self, window_panel):
        Tool.__init__(self, window_panel, pygame.image.load('icons/eraser_tool_icon.png'))

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()

        canvas_x, canvas_y = self.window_panel.raster_canvas.get_position_topleft()
        canvas_w, canvas_h = self.window_panel.raster_canvas.get_zoomed_size()

        if self.is_in_canvas_space(self.window_panel.mouse_pos, canvas_x, canvas_y, canvas_w, canvas_h) and not self.window_panel.tool_set.active:
            if mouse_pressed[0]:
                self.active = True
                self.window_panel.tool_set.active = True
                self.window_panel.inter_lock = True
                mouse_canvas_x, mouse_canvas_y = self.get_mouse_canvas_coordinates(self.window_panel.mouse_pos, canvas_x, canvas_y)
                self.window_panel.raster_canvas.pixel_buffer.set_at((mouse_canvas_x, mouse_canvas_y), pygame.Color(0, 0, 0, 0))
            elif self.active:
                self.active = False
                self.window_panel.tool_set.active = False
                self.window_panel.inter_lock = False

    def draw(self): 
        pass

class Fill(Tool):
    def __init__(self, window_panel):
        Tool.__init__(self, window_panel, pygame.image.load('icons/fill_tool_icon.png'))

    def is_in_array(self, array, item) -> bool:
        for i in array:
            if i == item:
                return True
        
        return False

    def fill_area(self, x, y):
        neighbouring_pixels = ((0, -1), (1, 0), (0, 1), (-1, 0))
        frontier = [(x, y)]
        reached = [(x, y)]
        check_color = self.window_panel.raster_canvas.pixel_buffer.get_at((x, y))
        fill_with_color = self.window_panel.palette.get_color()
        self.window_panel.raster_canvas.pixel_buffer.set_at((x, y), fill_with_color)

        while len(frontier) > 0:
            new_frontier = []
            for i in frontier:
                for j in neighbouring_pixels:
                    if i[0] + j[0] >= 0 and i[0] + j[0] < self.window_panel.raster_canvas.pixel_buffer.get_width() and i[1] + j[1] >= 0 and i[1] + j[1] < self.window_panel.raster_canvas.pixel_buffer.get_height() and self.window_panel.raster_canvas.pixel_buffer.get_at((i[0] + j[0], i[1] + j[1])) == check_color and not self.is_in_array(reached, (i[0] + j[0], i[1] + j[1])):
                        self.window_panel.raster_canvas.pixel_buffer.set_at((i[0] + j[0], i[1] + j[1]), fill_with_color)
                        new_frontier.append((i[0] + j[0], i[1] + j[1]))
                        reached.append((i[0] + j[0], i[1] + j[1]))
            frontier = new_frontier

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()

        canvas_x, canvas_y = self.window_panel.raster_canvas.get_position_topleft()
        canvas_w, canvas_h = self.window_panel.raster_canvas.get_zoomed_size()

        if self.is_in_canvas_space(self.window_panel.mouse_pos, canvas_x, canvas_y, canvas_w, canvas_h) and not self.window_panel.tool_set.active:
            if mouse_pressed[0]:
                self.active = True
                self.window_panel.tool_set.active = True
                self.window_panel.inter_lock = True
                mouse_canvas_x, mouse_canvas_y = self.get_mouse_canvas_coordinates(self.window_panel.mouse_pos, canvas_x, canvas_y)
                self.fill_area(mouse_canvas_x, mouse_canvas_y)
            elif self.active: 
                self.active = False
                self.window_panel.tool_set.active = False
                self.window_panel.inter_lock = False

    def draw(self): 
        pass

class Shape(Tool):
    def __init__(self, window_panel, width=0):
        self.icons = [pygame.image.load('icons/rect_shape_tool_icon.png'), pygame.image.load('icons/circle_shape_tool_icon.png'), 
                      pygame.image.load('icons/triangle_shape_tool_icon.png'), pygame.image.load('icons/rect_shape_outline_tool_icon.png'),
                      pygame.image.load('icons/circle_shape_outline_tool_icon.png'), pygame.image.load('icons/triangle_shape_outline_tool_icon.png')]
        if width != 0: Tool.__init__(self, window_panel, self.icons[3])
        else: Tool.__init__(self, window_panel, self.icons[0])
        self.shape_start = pygame.Vector2(0, 0)
        self.shape = 'rect'
        self.shapes = ['rect', 'circle', 'triangle']
        self.width = width

    def nextShape(self):
        for i in range(len(self.shapes)):
            if self.shapes[i] == self.shape:
                if i == len(self.shapes)-1:self.shape = self.shapes[0]
                else: self.shape = self.shapes[i+1]
                if self.width != 0: self.icon = self.icons[i+3]
                else: self.icon = self.icons[i]
                break 

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()

        canvas_x, canvas_y = self.window_panel.raster_canvas.get_position_topleft()
        canvas_w, canvas_h = self.window_panel.raster_canvas.get_zoomed_size()

        if self.is_in_canvas_space(self.window_panel.mouse_pos, canvas_x, canvas_y, canvas_w, canvas_h) and not self.window_panel.tool_set.active:
            mouse_canvas_x, mouse_canvas_y = self.get_mouse_canvas_coordinates(self.window_panel.mouse_pos, canvas_x, canvas_y)
            if mouse_pressed[0] and not self.active:
                self.active = True
                self.window_panel.tool_set.active = True
                self.window_panel.inter_lock = True
                self.shape_start.x = mouse_canvas_x
                self.shape_start.y = mouse_canvas_y
            elif mouse_pressed[0]:
                self.window_panel.raster_canvas.preview_buffer.fill(pygame.Color(0,0,0,0))
                if self.shape == 'rect':
                    pygame.draw.rect(self.window_panel.raster_canvas.preview_buffer, self.window_panel.palette.get_color(), [self.shape_start.x, self.shape_start.y, abs(mouse_canvas_x - self.shape_start.x)+1, abs(mouse_canvas_y - self.shape_start.y)+1], self.width)
                elif self.shape == 'circle':
                    pygame.draw.circle(self.window_panel.raster_canvas.preview_buffer, self.window_panel.palette.get_color(), [self.shape_start.x, self.shape_start.y], math.sqrt(math.pow(mouse_canvas_x-self.shape_start.x, 2) + math.pow(mouse_canvas_y-self.shape_start.y, 2))+1, self.width)
                elif self.shape == 'triangle':
                    pygame.draw.polygon(self.window_panel.raster_canvas.preview_buffer, self.window_panel.palette.get_color(), [(self.shape_start.x, self.shape_start.y), (mouse_canvas_x, mouse_canvas_y), (self.shape_start.x-(mouse_canvas_x-self.shape_start.x)+1, mouse_canvas_y)], self.width)
            elif self.active:
                self.window_panel.raster_canvas.blit_preview()
                self.window_panel.raster_canvas.preview_buffer.fill(pygame.Color(0,0,0,0))
                self.active = False
                self.window_panel.tool_set.active = False
                self.window_panel.inter_lock = False

    def draw(self):
        pass

class Picker(Tool):
    def __init__(self, window_panel):
        Tool.__init__(self, window_panel, pygame.image.load('icons/picker_tool_icon.png'))

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()

        canvas_x, canvas_y = self.window_panel.raster_canvas.get_position_topleft()
        canvas_w, canvas_h = self.window_panel.raster_canvas.get_zoomed_size()

        if self.is_in_canvas_space(self.window_panel.mouse_pos, canvas_x, canvas_y, canvas_w, canvas_h) and not self.window_panel.tool_set.active:
            if mouse_pressed[0]:
                self.active = True
                self.window_panel.tool_set.active = True
                self.window_panel.inter_lock = True
                mouse_canvas_x, mouse_canvas_y = self.get_mouse_canvas_coordinates(self.window_panel.mouse_pos, canvas_x, canvas_y)
                self.window_panel.palette.set_color(self.window_panel.raster_canvas.pixel_buffer.get_at((mouse_canvas_x, mouse_canvas_y)))
            elif self.active: 
                self.active = False
                self.window_panel.tool_set.active = False
                self.window_panel.inter_lock = False

    def draw(self): 
        pass