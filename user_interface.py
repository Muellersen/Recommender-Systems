import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from recommender_system import Recommender

# create the root window
root = tk.Tk()
root.geometry('1000x500')
root.resizable(True, True)
root.title('Filme Empfehler')

recommender = Recommender()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# create a list box
movies = recommender.get_movie_names()

movies_var = tk.StringVar(value=movies)

listbox = tk.Listbox(
    root,
    listvariable=movies_var,
    height=9,
    width=100,
    selectmode='extended')

listbox.pack()

def printInput():
    inp = inputtxt.get(1.0, "end-1c")
    search_result = recommender.search_movies(inp)

    search_result_str = ""
    for i in search_result:
        search_result_str += i + ", "

    lbl.config(text = "Suchergebnis: "+search_result_str)
  
# TextBox Creation
inputtxt = tk.Text(root,
                   height = 2,
                   width = 20)
  
inputtxt.pack()
  
# Button Creation
printButton = tk.Button(root,
                        text = "Print", 
                        command = printInput)
printButton.pack()
  
# Label Creation
lbl = tk.Label(root, text = "")
lbl.pack()

# movies = recommend(5)

# for movie in movies:
#     print(movielist.loc[movielist["movieId"] == movie[0]])

# handle event
def items_selected(event):
    """ handle item selected event
    """
    # get selected indices
    selected_indices = listbox.curselection()
    # get selected items
    selected_movies = ",".join([listbox.get(i) for i in selected_indices])
    msg = f'You selected: {selected_movies}'

    showinfo(
        title='Information',
        message=msg)


listbox.bind('<<ListboxSelect>>', items_selected)

root.mainloop()