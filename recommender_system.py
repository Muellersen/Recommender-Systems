from cmath import inf
import re
import pandas as pd
import numpy as np
from functools import cmp_to_key


class Recommender:
    def __init__(self):
        self.ratings = pd.read_csv('ml-latest-small/ratings.csv', low_memory=False)
        self.movies = pd.read_csv("ml-latest-small/movies.csv", low_memory=False)
        self.new_user = pd.read_csv("ml-latest-small/new.csv", low_memory=False)
        self.animes = pd.read_csv("archiveAnime/anime.csv", low_memory=False)
        self.anime_ratings = pd.read_csv("archiveAnime/rating.csv", low_memory=False)
    
    def create_new_user(self, userId: int, rated_movies: list):
        data = {"userId": [], "Id": [], "rating": []}
        for movie_and_rating in rated_movies:
            movie_name = movie_and_rating[0]
            rating = movie_and_rating[1]
            data["userId"] += [userId]
            data["Id"] += [movie_name] # or id?
            data["rating"] += [rating]
        df = pd.DataFrame(data=data)
        self.new_user = df
        print(self.new_user)

    def get_movie_names(self, anime=False) -> tuple:
        if anime:
            return tuple(self.animes["title"].to_list())
        return tuple(self.movies["title"].to_list())

    def compare(item1: tuple, item2: tuple):
        if item1[1] < item2[1]:
            return -1
        elif item1[1] > item2[1]:
            return 1
        else:
            return 0

    letter_cmp_key = cmp_to_key(compare)

    def k_nearest_neighbor(self, k: int, watched_same_movies: int, amount: int, anime=False) -> list:
        ratings = self.ratings
        if anime:
            ratings = self.anime_ratings
        new_user = self.new_user
        neighbors = []
        for user in range(1, amount):
            user_data = ratings.loc[ratings["userId"] == user]
            distances = []
            amount_same_movies = user_data["Id"].count()

            # print(amount_same_movies)
            for movie in user_data["Id"].iteritems():
                movie_id = movie[1]
                new_user_rating = new_user.loc[new_user["Id"] == movie_id]["rating"].tolist()

                if len(new_user_rating) == 0:
                    amount_same_movies -= 1
                    continue

                user_rating = user_data.loc[user_data["Id"] == movie_id]["rating"].tolist()
                if user_rating[0] == -1:
                    continue
                distance: float = user_rating[0] - new_user_rating[0]
                distances += [abs(distance)]

                # print(new_user_rating, user_rating)
            # print(distances)

            result = 0

            if len(distances) == 0:
                neighbors += [(user, inf)]
                continue

            for dis in distances:
                result += dis
            result /= len(distances)
            neighbors += [(user, result, amount_same_movies)]

        k_nearest_neighbors = []
        for i in range(k):
            nearest_neighbor = (inf, inf)
            current_index_of_nearest_neighbor = inf
            for j, neighbor in enumerate(neighbors):
                if neighbor[1] < nearest_neighbor[1] and neighbor[2] > watched_same_movies:
                    nearest_neighbor = neighbor
                    current_index_of_nearest_neighbor = j
            if current_index_of_nearest_neighbor != inf: del neighbors[current_index_of_nearest_neighbor]
            k_nearest_neighbors += [nearest_neighbor]

        return k_nearest_neighbors

    def recommend(self, amount: int, anime=False):
        ratings = self.ratings
        if anime:
            ratings = self.anime_ratings

        new_user = self.new_user

        similar_users = self.k_nearest_neighbor(10, 5, 600, anime)
        movies_of_users_the_new_user_didnt_watch = []
        movie_bucket = {}
        for user in similar_users:
            user_data = ratings.loc[ratings["userId"] == user[0]]
            movies = []
            for movie in user_data["Id"].iteritems():
                movie_id = movie[1]
                new_user_rating = new_user.loc[new_user["Id"] == movie_id]["Id"].tolist()
                user_rating = user_data.loc[user_data["Id"] == movie_id]["rating"].tolist()

                if len(new_user_rating) != 0:
                    continue

                movies += [(movie_id, user_rating[0])]
                if str(movie_id) in movie_bucket:
                    movie_bucket[str(movie_id)] = movie_bucket[str(movie_id)] + 1
                else:
                    movie_bucket[str(movie_id)] = 1

            movies_of_users_the_new_user_didnt_watch += [movies]

        best_movies = []
        for i in range(amount):
            best_movie = (None, -1)
            for movies in movies_of_users_the_new_user_didnt_watch:
                for movie in movies:
                    if str(movie[0]) not in movie_bucket:
                        continue

                    score = movie[1] + movie_bucket[str(movie[0])]
                    if score > best_movie[1] and str(movie[0]) in movie_bucket:
                        best_movie = (movie[0], score)
            if str(best_movie[0]) in movie_bucket:
                movie_bucket.pop(str(best_movie[0]))
            best_movies += [best_movie]
        return best_movies

    def search_movies(self, name: str, anime=False) -> list:
        movie_names = self.movies["title"]
        if anime:
            movie_names = self.animes["title"]
        result = []
        for movie in movie_names:
            match = re.search(name+".*", movie, re.IGNORECASE)
            if match:
                result += [movie]

        return result

    def k_nearest_neighbor_item(self, k: int, movieId: int, amount: int, anime=False) -> list:
        ratings = self.ratings
        if anime:
            ratings = self.anime_ratings
        new_user = self.new_user
        neighbors = []
        movie_data = ratings.loc[ratings["Id"] == movieId]
        movie_rating = np.ndarray()
        for user_id in range(73516):
            rating = movie_data.loc[movie_data["userId"] == user_id]
            if rating.empty:
                movie_rating[user_id] = -1
                continue
            movie_rating[user_id] = rating



# x = Recommender()
# x.k_nearest_neighbor_item(5, 5, 5, True)