import tkinter as tk
from tkinter import END, ttk
from tkinter.messagebox import showinfo
from recommender_system import Recommender


class GUI:
    def __init__(self, recommender: Recommender, anime=False):
        self.root = tk.Tk()
        self.recommender = recommender
        self.is_anime = anime
        self.all_movies = recommender.get_movie_names(anime)
        self.selected_movies = []
        self.selected_movies_ids = []
        self.selected_indices = []

    def init_window(self):
        self.root.geometry('1000x500')
        self.root.resizable(True, True)
        self.root.title('Filme Empfehler')

    def init_list(self):
        movies_var = tk.StringVar(value=self.all_movies)
        self.listbox = tk.Listbox(
            self.root,
            listvariable=movies_var,
            height=20,
            width=100,
            selectmode='single')
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

    def init_list_of_selected_items(self):
        selected_movies_var = tk.StringVar(value=self.selected_movies)
        self.listbox_of_selected_items = tk.Listbox(
            self.root,
            listvariable=selected_movies_var,
            height=20,
            width=100,
            selectmode='single')
        self.listbox_of_selected_items.pack(side="left")
        self.listbox_of_selected_items.bind('<<ListboxSelect>>', self.items_selected_of_selected_movies_list)

    def init_list_of_recommended_movies(self):
        recommended = tk.StringVar(value=self.selected_movies)
        self.listbox_of_recommended_movies = tk.Listbox(
            self.root,
            listvariable=recommended,
            height=20,
            width=100,
            selectmode='single')
        self.listbox_of_recommended_movies.pack(side="right")

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
                        text="Auswahl löschen",
                        command=self.reset_selection)
        self.rate_button.pack()

    def init_recommend_button(self):
        self.recommend_button = tk.Button(self.root,
                        text="Empfehlung",
                        command=self.start_recommendation)
        self.recommend_button.pack()

    def init_label(self):
        self.label = tk.Label(self.root, text="")
        self.label.pack()

    def update_list(self, movies: tuple):
        self.listbox.delete(0, END)
        for i, movie in enumerate(movies):
            self.listbox.insert(i, movie)
        
    def update_list_of_selected_movies(self):
        self.listbox_of_selected_items.delete(0, END)
        for i, movie in enumerate(self.selected_movies):
            self.listbox_of_selected_items.insert(i, movie)

    def update_list_of_recommended_movies(self, recommended_movies: list):
        self.listbox_of_recommended_movies.delete(0, END)
        for i, movie in enumerate(recommended_movies):
            self.listbox_of_recommended_movies.insert(i, movie)

    def reset_selection(self):
        self.selected_movies = []
        self.selected_movies_ids = []

    def search(self):
        inp = self.inputtxt.get(1.0, "end-1c")
        search_result = self.recommender.search_movies(inp, self.is_anime)
        self.update_list(tuple(search_result))

    def get_movie_ids(self):
        self.selected_movies_ids = []
        if self.is_anime:
            for movie in self.selected_movies:
                self.selected_movies_ids += self.recommender.animes.loc[self.recommender.animes["title"] == movie]["Id"].to_list()
        else:
            for movie in self.selected_movies:
                self.selected_movies_ids += self.recommender.movies.loc[self.recommender.movies["title"] == movie]["Id"].to_list()
        print(self.selected_movies_ids)

    def items_selected(self, event):
        """ handle item selected event
        """
        selected_indices = self.listbox.curselection()
        # selected_movies = ", ".join([self.listbox.get(i) for i in selected_indices])
        self.selected_movies += [self.listbox.get(i) for i in selected_indices]
        self.update_list_of_selected_movies()
        print(self.selected_movies)

    def items_selected_of_selected_movies_list(self, event):
        """ handle item selected event
        """
        selected_indices = self.listbox_of_selected_items.curselection()
        # selected_movies = ", ".join([self.listbox.get(i) for i in selected_indices])
        movie_to_delete = [self.listbox_of_selected_items.get(i) for i in selected_indices]

        for i, movie in enumerate(self.selected_movies):
            if movie == movie_to_delete[0]:
                del self.selected_movies[i]
        self.update_list_of_selected_movies()

    def start_recommendation(self):
        self.get_movie_ids()
        movie_rating = []
        for movie in self.selected_movies_ids:
            if self.is_anime:
                movie_rating += [(movie, 10)]
            else:
                movie_rating += [(movie, 5)]
        self.recommender.create_new_user(1, movie_rating)
        recommendation = self.recommender.recommend(5, self.is_anime)
        print(recommendation)
        result = ""
        result2 = []
        if self.is_anime:
            for movie in recommendation:
                result += self.recommender.animes.loc[self.recommender.animes["Id"] == movie[0]]["title"].to_string() + ", "
                result2 += [self.recommender.animes.loc[self.recommender.animes["Id"] == movie[0]]["title"].to_string()]
        else:
            for movie in recommendation:
                result += self.recommender.movies.loc[self.recommender.movies["Id"] == movie[0]]["title"].to_string() + ", "
                result2 += [self.recommender.movies.loc[self.recommender.movies["Id"] == movie[0]]["title"].to_string()]
        self.label.config(text = "Empfehlung: "+result)
        self.update_list_of_recommended_movies(result2)

    def init_all(self):
        self.init_window()
        self.init_list()
        self.init_text_field()
        self.init_search_button()
        self.init_rate_button()
        self.init_recommend_button()
        self.init_label()
        self.init_list_of_selected_items()
        self.init_list_of_recommended_movies()#

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
# #     print(movielist.loc[movielist["Id"] == movie[0]])

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