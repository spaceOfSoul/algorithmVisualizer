import pygame as pg
import random
import math

pg.init()

class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255, 0, 0
    BACKGROUNDCOLOR = BLACK
    
    GRADIENT = [
        (128,128,128)#gray
        ,(160,160,160)
        ,(192,192,192)
    ]
    
    FONT = pg.font.SysFont('arial',20)
    LARGE_FONT = pg.font.SysFont('arial',30)
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
        
        self.block_width = math.floor((self.width - self.SIDE_PAD)/ len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD //2
        
def draw(draw_info : DrawInformation,algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUNDCOLOR)
    
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'ascending' if ascending else 'descending'}",1,draw_info.WHITE)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 ,5))
    
    control = draw_info.FONT.render("R - Reroll | SPACE - Start sorting | A - ascending and descending",1,draw_info.WHITE)
    draw_info.window.blit(control, (draw_info.width/2 - control.get_width()/2 ,35))
    
    sortings = draw_info.FONT.render("I - Insertion Sort | B - Bubble sort | Q - Qucik sort",1,draw_info.WHITE)
    draw_info.window.blit(sortings, (draw_info.width/2 - sortings.get_width()/2 ,65))
    
    draw_list(draw_info, draw_info.lst)
    pg.display.update()
    
def draw_list(draw_info : DrawInformation, lst, color_position={}, clear_bg=False):
    
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pg.draw.rect(draw_info.window, draw_info.BACKGROUNDCOLOR, clear_rect)
    
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        
        color = draw_info.GRADIENT[i%3]
        
        if i in color_position:
            color = color_position[i]
        
        pg.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pg.display.update()

def generate_starting_list(n, minVal, maxVal):
    lst = []
    for _ in range(n):
        val = random.randint(minVal, maxVal)
        lst.append(val)
    return lst

#sorting algorithms---------------------------------------------------
def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    
    length = len(lst)
    for i in range(length-1):
        for j in range(length - 1,i,-1):
            if (lst[j-1] > lst[j] and ascending) or (lst[j-1] < lst[j] and not ascending):
                lst[j-1], lst[j] = lst[j], lst[j-1]
                draw_list(draw_info,lst, {j: draw_info.GREEN, j-1 : draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, acsending = True):
    lst = draw_info.lst
    length = len(lst)
    
    for i in range(1, length):
        current = lst[i]
        
        while(True):
            acsending_sort  = i > 0 and lst[i-1] > current and acsending
            decsending_sort  = i > 0 and lst[i-1] < current and not acsending
            
            if not acsending_sort and not decsending_sort:
                break
            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current
            draw_list(draw_info,lst, {i-1: draw_info.GREEN, i : draw_info.RED}, True)
            yield True
    return lst



def quick_sort(draw_info, acsending = True):
    def qsort(draw_info,lst,left,right,asc):
        pl = left
        pr = right
        x = lst[(left + right) // 2]
    
        while pl <= pr:
            if asc:
                while lst[pl] < x: pl += 1
                while lst[pr] > x: pr -= 1
            else:
                while lst[pl] > x: pl += 1
                while lst[pr] < x: pr -= 1
            if pl<=pr:
                lst[pl],lst[pr] = lst[pr],lst[pl]
                draw_list(draw_info,lst, {pl: draw_info.GREEN, pr : draw_info.RED}, True)
                pl+=1
                pr-=1

        if left <pr: qsort(draw_info,lst, left, pr,asc)
        if pl < right: qsort(draw_info,lst, pl,right,asc)
    qsort(draw_info,draw_info.lst,0,len(draw_info.lst)-1,acsending)

#---------------------------------------------------------------------
def main():
    run = True
    clock = pg.time.Clock()
    
    n = 100
    min_val = 0
    max_val = 100
    
    lst = generate_starting_list(n,min_val,max_val)
    draw_info = DrawInformation(800,600, lst)
    sorting = False
    ascending = True
    
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble_sort"
    sorting_algorithm_generator = None
    
    while run:
        clock.tick(30)#fps
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                
            if event.type != pg.KEYDOWN:
                continue
            
            if event.key == pg.K_r:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pg.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
            elif event.key == pg.K_a and not sorting:
                ascending = not ascending
            elif event.key == pg.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble_sort"
            elif event.key == pg.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insert_sort"
            elif event.key == pg.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "Quick_sort"
            
    pg.quit()

if __name__ == "__main__":
    main()