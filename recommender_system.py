from cmath import inf
import re
import pandas as pd
import numpy as np
from functools import cmp_to_key


class Recommender:
    def __init__(self):
        self.metadata = pd.read_csv('ml-latest-small/ratings.csv', low_memory=False)
        self.movies = pd.read_csv("ml-latest-small/movies.csv", low_memory=False)
        self.new_user = pd.read_csv("ml-latest-small/new.csv", low_memory=False)
    
    def create_new_user(self, userId: int, rated_movies: list):
        data = {"userId": [], "movieId": [], "ratings": []}
        for movie_and_rating in rated_movies:
            movie_name = movie_and_rating[0]
            rating = movie_and_rating[1]
            data["userId"] += [userId]
            data["movieId"] += [movie_name] # or id?
            data["ratings"] += [rating]
        df = pd.DataFrame(data=data)
        self.new_user = df

    def get_movie_names(self) -> tuple:
        return tuple(self.movies["title"].to_list())

    def compare(item1: tuple, item2: tuple):
        if item1[1] < item2[1]:
            return -1
        elif item1[1] > item2[1]:
            return 1
        else:
            return 0

    letter_cmp_key = cmp_to_key(compare)

    def k_nearest_neighbor(self, k: int, watched_same_movies: int, amount: int) -> list:
        metadata = self.metadata
        new_user = self.new_user
        neighbors = []
        for user in range(1, amount):
            user_data = metadata.loc[metadata["userId"] == user]
            distances = []
            amount_same_movies = user_data["movieId"].count()

            # print(amount_same_movies)
            for movie in user_data["movieId"].iteritems():
                movie_id = movie[1]
                new_user_rating = new_user.loc[new_user["movieId"] == movie_id]["rating"].tolist()

                if len(new_user_rating) == 0:
                    amount_same_movies -= 1
                    continue

                user_rating = user_data.loc[user_data["movieId"] == movie_id]["rating"].tolist()
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
            del neighbors[current_index_of_nearest_neighbor]
            k_nearest_neighbors += [nearest_neighbor]

        return k_nearest_neighbors

    def recommend(self, amount: int):
        metadata = self.metadata
        new_user = self.new_user

        similar_users = self.k_nearest_neighbor(10, 10, 50)
        movies_of_users_the_new_user_didnt_watch = []
        movie_bucket = {}
        for user in similar_users:
            user_data = metadata.loc[metadata["userId"] == user[0]]
            movies = []
            for movie in user_data["movieId"].iteritems():
                movie_id = movie[1]
                new_user_rating = new_user.loc[new_user["movieId"] == movie_id]["movieId"].tolist()
                user_rating = user_data.loc[user_data["movieId"] == movie_id]["rating"].tolist()

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

    def search_movies(self, name: str) -> list:  # doesnt get the full string of the title
        movie_names = self.movies["title"]
        return [itm[0] for itm in movie_names.str.findall(name + ".*", flags=re.IGNORECASE) if len(itm)>0]