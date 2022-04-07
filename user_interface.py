import tkinter as tk
from tkinter import END, ttk
from tkinter.messagebox import showinfo
from recommender_system import Recommender


class GUI:
    def __init__(self, recommender: Recommender):
        self.root = tk.Tk()
        self.recommender = recommender
        self.all_movies = recommender.get_movie_names()
        self.selected_movies = []

    def init_window(self):
        self.root.geometry('1000x500')
        self.root.resizable(True, True)
        self.root.title('Filme Empfehler')

    def init_list(self):
        movies_var = tk.StringVar(value=self.all_movies)
        self.listbox = tk.Listbox(
            self.root,
            listvariable=movies_var,
            height=9,
            width=100,
            selectmode='multiple')
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

    def init_text_field(self):
        self.inputtxt = tk.Text(self.root,
                   height=2,
                   width=20)
        self.inputtxt.pack()

    def init_search_button(self):
        self.printButton = tk.Button(self.root,
                        text="Suche",
                        command=self.search)
        self.printButton.pack()

    def init_rate_button(self):
        self.rate_button = tk.Button(self.root,
                        text="Bewerten",
                        command=self.search)
        self.rate_button.pack()

    def init_recommend_button(self):
        self.recommend_button = tk.Button(self.root,
                        text="Empfehlung",
                        command=self.recommender.recommend(1))
        self.recommend_button.pack()

    def init_label(self):
        self.label = tk.Label(self.root, text="")
        self.label.pack()

    def update_list(self, movies: tuple):
        self.listbox.delete(0, END)
        for i, movie in enumerate(movies):
            self.listbox.insert(i, movie)

    def search(self):
        inp = self.inputtxt.get(1.0, "end-1c")
        search_result = self.recommender.search_movies(inp)
        self.update_list(tuple(search_result))

    def items_selected(self, event):
        """ handle item selected event
        """
        selected_indices = self.listbox.curselection()
        # selected_movies = ", ".join([self.listbox.get(i) for i in selected_indices])
        self.selected_movies = [self.listbox.get(i) for i in selected_indices]

    def init_all(self):
        self.init_window()
        self.init_list()
        self.init_search_button()
        self.init_text_field()

# # create the root window
# root = tk.Tk()
# root.geometry('1000x500')
# root.resizable(True, True)
# root.title('Filme Empfehler')

# recommender = Recommender()

# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# # create a list box
# movies = recommender.get_movie_names()

# movies_var = tk.StringVar(value=movies)

# listbox = tk.Listbox(
#     root,
#     listvariable=movies_var,
#     height=9,
#     width=100,
#     selectmode='extended')

# listbox.pack()


# def printInput():
#     inp = inputtxt.get(1.0, "end-1c")
#     search_result = recommender.search_movies(inp)

#     search_result_str = ""
#     for i in search_result:
#         search_result_str += i + ", "

#     lbl.config(text = "Suchergebnis: "+search_result_str)
  
  
# # TextBox Creation
# inputtxt = tk.Text(root,
#                    height = 2,
#                    width = 20)
  
# inputtxt.pack()
  
# # Button Creation
# printButton = tk.Button(root,
#                         text = "Print", 
#                         command = printInput)
# printButton.pack()
  
# # Label Creation
# lbl = tk.Label(root, text = "")
# lbl.pack()

# # movies = recommend(5)

# # for movie in movies:
# #     print(movielist.loc[movielist["movieId"] == movie[0]])

# # handle event
# def items_selected(event):
#     """ handle item selected event
#     """
#     # get selected indices
#     selected_indices = listbox.curselection()
#     # get selected items
#     selected_movies = ",".join([listbox.get(i) for i in selected_indices])
#     msg = f'You selected: {selected_movies}'

#     showinfo(
#         title='Information',
#         message=msg)


# listbox.bind('<<ListboxSelect>>', items_selected)

# root.mainloop()