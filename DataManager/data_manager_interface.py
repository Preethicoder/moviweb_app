from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def add_movie(self, movie_name, movie_director, year, rating, user_id):
        pass

    @abstractmethod
    def update_movie(self, movie_id, **kwargs):
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        pass
