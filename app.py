from tkinter import *
import sortingVisualze

root = Tk()
root.title("algorithm visualizer")
root.geometry('400x300')

btn_sort = Button(root, padx=10, pady=50,width=200, height=100, text="Sorting", command=sortingVisualze.main )
btn_sort.pack()

root.mainloop()