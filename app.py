import pygame as pg
import random

pg.init()

class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 128, 128, 128
    BACKGROUNDCOLOR = WHITE
    
    GRADIENT = [
        (128,128,128)#gray
        ,(160,160,160)
        ,(192,192,192)
    ]
    
    SIDE_PAD = 100
    TOP_PAD = 150
    
    def __init__(self, width, hegit, lst):
        self.width = width
        self.height = hegit
        self.window = pg.display.set_mode((width,hegit))
        pg.display.set_caption("sorting algorithm Visualization")
        self.set_list(lst)
    
    
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        
        self.block_width = round((self.width - self.SIDE_PAD)/ len(lst))
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD //2
        
def draw(draw_info : DrawInformation):
    draw_info.window.fill(draw_info.BACKGROUNDCOLOR)
    draw_list(draw_info)
    pg.display.update()
    
def draw_list(draw_info : DrawInformation):
    lst = draw_info.lst
    
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        
        color = draw_info.GRADIENT[i%3]
        
        pg.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

def generate_starting_list(n, minVal, maxVal):
    lst = []
    for _ in range(n):
        val = random.randint(minVal, maxVal)
        lst.append(val)
    return lst

def main():
    run = True
    clock = pg.time.Clock()
    
    n = 50
    min_val = 0
    max_val = 100
    
    lst = generate_starting_list(n,min_val,max_val)
    draw_info = DrawInformation(800,600, lst)
    
    while run:
        clock.tick(60)#fps
        
        draw(draw_info)
        
        for event in pg.event.get():
            if event == pg.QUIT:
                run = False
            
    pg.quit()

if __name__ == "__main__":
    main()