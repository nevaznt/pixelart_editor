import pygame
from sys import exit
from canvas import Raster_canvas
from toolset import Tool_set
from palette import Palette
from export import Export
from create import Create

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080

class Window_panel:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.create = None
        self.raster_canvas = None
        self.tool_set = None
        self.palette = None
        self.export = None
        self.mousewheel = 0
        self.mouse_rel = (0, 0)
        self.mouse_pos = (0, 0)
        self.inter_lock = False
        self.in_editing = False

    def update(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT

        SCREEN_WIDTH = self.screen.get_width()
        SCREEN_HEIGHT = self.screen.get_height()
        self.mouse_rel = pygame.mouse.get_rel()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mousewheel = 0
        pygame.display.update()
        self.clock.tick(60)
    
    def editing_init(self, canvas_width, canvas_height):
        self.raster_canvas = Raster_canvas(canvas_width, canvas_height)
        self.raster_canvas.set_position_center(SCREEN_WIDTH, SCREEN_HEIGHT)
        while self.raster_canvas.WIDTH * self.raster_canvas.zoom < SCREEN_WIDTH/2 and self.raster_canvas.HEIGHT * self.raster_canvas.zoom < SCREEN_HEIGHT/2:
            self.raster_canvas.zoomin(0.01)
        self.tool_set = Tool_set(self)
        self.palette = Palette(self)
        self.palette.hex_input.update_color_value()
        self.export = Export(self)

        self.in_editing = True

    def creating(self):
        self.create.update()

        self.create.draw()

    def editing(self):
        self.screen.fill("#353535")

        if not self.inter_lock or self.tool_set.active:
            self.tool_set.update()
        if not self.inter_lock or self.palette.active:
            self.palette.update()
        self.raster_canvas.update(self)

        self.raster_canvas.draw(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.palette.draw()
        self.tool_set.draw()

        self.export.update()

def start_init(wp: Window_panel):
    pygame.init()
    wp.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    wp.clock = pygame.time.Clock()
    wp.create = Create(wp)

def stop_and_quit():
    pygame.quit()
    exit()

def main():
    window_panel = Window_panel()

    start_init(window_panel)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_and_quit()
            if event.type == pygame.MOUSEWHEEL:
                window_panel.mousewheel = event.y

        if window_panel.in_editing: window_panel.editing()
        else: window_panel.creating()

        window_panel.update()

main()
