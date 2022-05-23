from tkinter import *
import sortingVisualze

root = Tk()
root.title("algorithm visualizer")
root.geometry('400x300')

pushed  = False

def btn_push(func):
    global pushed
    if pushed:
        print('window is not exist.')
        return None
    else:
        pushed = True
        return func

btn_sort = Button(root, padx=10, pady=50, text="Sorting", command= btn_push(sortingVisualze.main ))
btn_sort.pack()
btn_traversal=Button(root, padx=10, pady=50, text="Graph traversal", command= btn_push(sortingVisualze.main ))
btn_traversal.pack()

root.mainloop()