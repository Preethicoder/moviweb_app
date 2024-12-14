from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Create an instance of SQLAlchemy


class User(db.Model):  # Inherit from db.Model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return f"{self.name}"


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(100))
    movie_director = db.Column(db.String(50))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Movie {self.movie_name} (Director: {self.movie_director}, Year: {self.year}, Rating: {self.rating})>"

    def __str__(self):
        return f"{self.movie_name} ({self.year}), directed by {self.movie_director}, rated {self.rating}/10"
