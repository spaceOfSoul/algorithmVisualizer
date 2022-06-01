from tkinter import *
import sortingVisualze
from importlib import reload

root = Tk()
root.title("algorithm visualizer")
root.geometry('400x300')

pushed  = False

def btn_push(module):
    global pushed
    reload(module)
    if pushed:
        print('window is not exist.')
        return None
    else:
        pushed = True
        return module.main

btn_sort = Button(root, padx=10, pady=50, text="Sorting", command= btn_push(sortingVisualze ))
btn_sort.pack()
btn_traversal=Button(root, padx=10, pady=50, text="Graph traversal", command= print('test1'))
btn_traversal.pack()

root.mainloop()