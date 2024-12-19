from flask import Flask, flash
from flask import request, url_for, redirect, render_template

from DataManager.sqlite_datamanager import SQLiteDataManager

app = Flask(__name__)
data_manger = SQLiteDataManager("library.sqlite")
app.secret_key = 'flask_orm'
API_KEY = 'f21eaff'


@app.route('/')
def home():
    return render_template("home_page.html")


@app.route('/users')
def list_users():
    """display list of users in the database"""
    users = data_manger.get_all_users()  # Get all users from the database
    print(users)
    return render_template("users_list.html", users=users)  # Pass users to a template


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """to add new user to database"""
    if request.method == 'POST':
        user_name = request.form['name'].strip() # Get the name from the form
        data_manger.add_user(user_name)  # Add the user to the database
        flash('User added successfully!', 'success')
        return redirect(url_for('list_users'))  # Redirect to users list
    return render_template("add_user.html")  # Show the form for adding a user


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """for given user_id it gives list of their favorite movies"""
    user = data_manger.get_user_by_id(user_id)  # Get user by ID
    if user:
        movies = data_manger.get_user_movies(user_id)  # Get movies for the specific user
        return render_template("user_movies.html", user=user, movies=movies)
    return "User not found", 404


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """for a given user_id it add movie to database"""
    user = data_manger.get_user_by_id(user_id)  # Get user by ID
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        movie_name = request.form['movie_name'].strip()
        movie_director = request.form['movie_director'].strip()
        year = request.form['year'].strip()
        rating = request.form['rating'].strip()
        data_manger.add_movie(movie_name, movie_director, year, rating, user_id)  # Add movie
        flash('Movie added successfully!', 'success')
        return redirect(url_for('user_movies', user_id=user_id))  # Redirect to user’s movie list
    return render_template("add_movie.html", user=user_id)  #


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """ for existing movie we can update the parameter"""
    user = data_manger.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    movie = data_manger.get_movie_by_id(movie_id)
    if not movie or movie.user_id != user_id:
        return "Movie not found", 404

    if request.method == 'POST':
        movie_name = request.form['movie_name'].strip()
        movie_director = request.form['movie_director'].strip()
        year = request.form['year'].strip()
        rating = request.form['rating'].strip()
        updated_movie = data_manger.update_movie(movie_id, movie_name=movie_name,
                                                 movie_director=movie_director, year=year,
                                                 rating=rating)
        flash('Movie updated successfully!', 'success')
        # Redirect back to user’s movie list
        return redirect(url_for('user_movies', user_id=user_id))
        # Show form for updating movie
    return render_template("update_movie.html", user=user, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """for given user_id and movie_id it delete the movie from database"""
    user = data_manger.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    movie = data_manger.get_movie_by_id(movie_id)
    if not movie or movie.user_id != user_id:
        return "Movie not found", 404

    if request.method == 'POST':
        data_manger.delete_movie(movie_id)  # Delete movie from the database
        flash('Movie deleted successfully!', 'success')
        return redirect(url_for('user_movies', user_id=user_id))  # Redirect back to user’s movie list

    return render_template("delete_movie.html", user=user, movie=movie)  # Confirmation form


@app.errorhandler(404)
def page_not_found(e):
    """page not found"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error():
    """internal server error"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
