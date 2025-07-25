import pygame
import png
import tkinter as tk
from tkinter import filedialog

class Export:
    def __init__(self, window_panel):
        self.window_panel = window_panel
        
    def get_file_path(self):
        root = tk.Tk()
        root.withdraw()

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Export Image"
        )
        return path

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
            path = self.get_file_path()
            if path == '': return

            canvas = self.window_panel.raster_canvas.pixel_buffer
            buffer = []
            for i in range(canvas.get_height()):
                row = ()
                for j in range(canvas.get_width()):
                    row = row + ((canvas.get_at((j, i)).r, canvas.get_at((j, i)).g, canvas.get_at((j, i)).b, canvas.get_at((j, i)).a))
                buffer.append(row)
            image = png.from_array(buffer, "RGBA;8")
            image.save(path)