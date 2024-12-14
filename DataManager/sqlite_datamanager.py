import os

from flask import Flask
from sqlalchemy import inspect

from DataManager import data_models
# Assuming User and Movie models are in a file called models.py
from DataManager.data_manager_interface import DataManagerInterface
from DataManager.data_models import User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        # Initialize Flask app and database connection
        self.app = Flask(__name__)

        basedir = os.path.abspath(os.path.dirname(__file__))
        db_directory = os.path.join(basedir, 'data')

        # Ensure the directory exists
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)

        db_path = os.path.join(db_directory, db_file_name)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialize SQLAlchemy
        self.db = data_models.db
        self.db.init_app(self.app)

        # Create tables if they don't already exist
        with self.app.app_context():
            self.db.create_all()

            # Inspect the tables after creating
            inspector = inspect(self.db.engine)
            print("Tables in database:", inspector.get_table_names())

    def get_user_by_id(self, user_id):
        """
        Retrieves a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to fetch.

        Returns:
            User: The user object if found, else None.
        """
        # Query the User model for the given user_id
        with self.app.app_context():
            user = User.query.filter_by(id=user_id).first()
            print(user)

            # Return the user object or None if no user is found
            return user

    def get_movie_by_id(self, movie_id):

        with self.app.app_context():
            movie = Movie.query.filter_by(id=movie_id).first()
            print(movie)
            return movie

    def get_all_users(self):
        """Retrieve all users from the database."""
        with self.app.app_context():
            return User.query.all()

    def get_user_movies(self, user_id):
        """Retrieve all movies for a specific user."""
        with self.app.app_context():
            return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, name):
        """Add a new user to the database."""
        with self.app.app_context():
            new_user = User(name=name)
            self.db.session.add(new_user)
            self.db.session.commit()  # Commit to save the user
            self.db.session.refresh(new_user)  # Ensure the user is fully loaded with all its attributes
            return new_user

        # Add a new movie

    def add_movie(self, movie_name, movie_director, year, rating, user_id):
        """Add a new movie to the database."""
        with self.app.app_context():
            new_movie = Movie(
                movie_name=movie_name,
                movie_director=movie_director,
                year=year,
                rating=rating,
                user_id=user_id
            )
            self.db.session.add(new_movie)
            self.db.session.commit()
            self.db.session.refresh(new_movie)
            return new_movie

    # Update movie details
    def update_movie(self, movie_id, **kwargs):
        """Update the details of a specific movie."""
        with self.app.app_context():
            movie = Movie.query.get(movie_id)
            if not movie:
                return None
            for key, value in kwargs.items():
                if hasattr(movie, key):
                    setattr(movie, key, value)
            self.db.session.commit()
            # Refresh the movie object to ensure it's updated and bound to the session
            self.db.session.refresh(movie)
            return movie

    # Delete a movie
    def delete_movie(self, movie_id):
        """Delete a specific movie from the database."""
        with self.app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                self.db.session.delete(movie)
                self.db.session.commit()
                return True
            return False

    def close_session(self):
        """Close the SQLAlchemy session."""
        with self.app.app_context():
            self.db.session.remove()


def main():
    # Step 1: Initialize SQLiteDataManager
    db_file_name = "movie_library.sqlite"  # SQLite database file
    data_manager = SQLiteDataManager(db_file_name)

    # Add a new user and retrieve all users
    user = data_manager.add_user("Alice")
    print(user)

    users = data_manager.get_all_users()
    print("All Users:", users)

    # Add a movie for the user
    movie = data_manager.add_movie("Inception", "Christopher Nolan", 2010, 8.8, user.id)
    print(movie)

    # Get movies for the user
    user_movies = data_manager.get_user_movies(user.id)
    print("User's Movies:", user_movies)

    # Update a movie
    updated_movie = data_manager.update_movie(movie.id, movie_name="Inception (Updated)", rating=9.0)
    print(f"Updated Movie: {updated_movie}")

    # Delete a movie
    is_deleted = data_manager.delete_movie(movie.id)
    print(f"Movie Deleted: {is_deleted}")


if __name__ == "__main__":
    main()
