import random
import pygame as pg
import sys
print(sys.setrecursionlimit(10**5))

pg.init()

class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255, 0, 0
    BACKGROUNDCOLOR = BLACK
    
    FONT = pg.font.SysFont('arial',20)
    LARGE_FONT = pg.font.SysFont('arial',30)
    SIDE_PAD = 100
    TOP_PAD = 150
    
    def __init__(self, width, hegit, lst):
        self.width = width
        self.height = hegit
        self.window = pg.display.set_mode((width,hegit), flags=pg.DOUBLEBUF)
        pg.display.set_caption("sorting algorithm Visualization")
        self.set_list(lst)
    
    
    def set_list(self, lst):
        self.lst = lst
        self.n = len(lst)
        self.block_width =(self.width - self.SIDE_PAD)/self.n
        print(self.block_width)
        self.block_height = (self.height - self.TOP_PAD) / self.n
        self.start_x = self.SIDE_PAD //2
        
def draw(draw_info : DrawInformation,algo_name,frame, ascending, hidden = False):
    draw_info.window.fill(draw_info.BACKGROUNDCOLOR)
    
    if not hidden:
        title = draw_info.LARGE_FONT.render(f"{algo_name} - {'ascending' if ascending else 'descending'}",1,draw_info.WHITE)
        draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2-350 ,5))
    
        speed = draw_info.LARGE_FONT.render(f"Speed x{frame/60}",1,draw_info.WHITE)
        draw_info.window.blit(speed, (draw_info.width/2 - title.get_width()/2-350 ,35))
    
        control = draw_info.FONT.render("R - Reroll | SPACE - Start sorting | A - ascending and descending",1,draw_info.WHITE)
        draw_info.window.blit(control, (draw_info.width/2 - control.get_width()/2+250 ,5))
    
        sortings = draw_info.FONT.render("I - Insertion Sort | B - Bubble sort | Q - Qucik sort | M - Merge sort | S - Selection sort",1,draw_info.WHITE)
        draw_info.window.blit(sortings, (draw_info.width/2 - sortings.get_width()/2+180 ,35))
    
        item_amount = draw_info.LARGE_FONT.render(f"Item amount : {draw_info.n}",1,draw_info.WHITE)
        draw_info.window.blit(item_amount, (draw_info.width/2 - title.get_width()/2-350 ,65))
    
    draw_list(draw_info, draw_info.lst)
    pg.display.update()
    
def draw_list(draw_info : DrawInformation, lst, color_position={}, clear_bg=False):
    UNDER = 10
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD-UNDER, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pg.draw.rect(draw_info.window, draw_info.BACKGROUNDCOLOR, clear_rect)
    
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - val * draw_info.block_height
        
        color = draw_info.WHITE
        
        if i in color_position:
            color = color_position[i]
        
        pg.draw.rect(draw_info.window, color, (x, y-UNDER, draw_info.block_width, draw_info.height-UNDER))
    
    if clear_bg:
        pg.display.update()

def generate_starting_list(n):
    lst = [i for i in range(n)]
    random.shuffle(lst)
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
    lst = draw_info.lst
    asc = acsending
    def qsort(left,right):
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

        if left <pr: qsort( left, pr)
        if pl < right: qsort( pl,right)
        return True
    yield qsort(0,len(lst)-1)
    
def merge_sort(draw_info, acsending = True):
    lst = draw_info.lst
    asc = acsending
    def _merge_sort(left,right):
        if left < right:
            mid = (left+right)//2
            
            _merge_sort(left,mid)
            _merge_sort(mid+1, right)
            
            p=j=0
            i=k=left
            
            while i<=mid:
                buff[p] = lst[i]
                p+=1
                i+=1
            
            while i <= right and j < p:
                if asc:
                    if buff[j] <= lst[i]:
                        lst[k] = buff[j]
                        j+=1
                        draw_list(draw_info,lst, {k: draw_info.GREEN, j : draw_info.RED}, True)
                    else:
                        lst[k] = lst[i]
                        i+=1
                        draw_list(draw_info,lst, {k: draw_info.GREEN, i : draw_info.RED}, True)
                else:
                    if buff[j] >= lst[i]:
                        lst[k] = buff[j]
                        j+=1
                        draw_list(draw_info,lst, {k: draw_info.GREEN, j : draw_info.RED}, True)
                    else:
                        lst[k] = lst[i]
                        i+=1
                        draw_list(draw_info,lst, {k: draw_info.GREEN, i : draw_info.RED}, True)
                k+=1
            
            while j<p:
                lst[k] = buff[j]
                k += 1
                j += 1
        return True
    
    n=len(lst)
    buff = [None]*n
    yield _merge_sort(0,n-1)
    
def selection_sort(draw_info, acsending = True):
    lst = draw_info.lst
    n = len(lst)
    for i in range(n-1):
        least = i
        for j in range(i+1, n):
            if (lst[j] < lst[least] and acsending) or (lst[j] > lst[least] and not acsending):
                least = j
    
        if i != least:
            lst[i], lst[least] = lst[least], lst[i]
            draw_list(draw_info,lst, {i: draw_info.GREEN, least : draw_info.RED}, True)
            yield True

def main():
    run = True
    clock = pg.time.Clock()
    
    n = 250
    
    lst = generate_starting_list(n)
    draw_info = DrawInformation(1024,600, lst)
    sorting = False
    ascending = True
    frame = 60
    
    HIDDEN = False
    
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble_sort"
    sorting_algorithm_generator = None
    
    while run:
        clock.tick(frame)#fps
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name,frame, ascending, HIDDEN)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                
            if event.type != pg.KEYDOWN:
                continue
            
            if event.key == pg.K_r:
                lst = generate_starting_list(n)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pg.K_F3:
                n-=5
                lst = generate_starting_list(n)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pg.K_F4:
                n+=5
                lst = generate_starting_list(n)
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
            elif event.key == pg.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algorithm_name = "Merge_sort"
            elif event.key == pg.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection_sort"
            elif event.key == pg.K_UP and not sorting:
                frame+=30
            elif event.key == pg.K_DOWN and not sorting:
                frame-=30
            elif event.key == pg.K_h and not sorting:
                HIDDEN = not HIDDEN
      
    pg.quit()

if __name__ == "__main__":
    main()