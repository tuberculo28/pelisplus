from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from flaskr.db import get_db

bp = Blueprint('film', __name__)

@bp.route('/')
def index():
    db = get_db()
    movies = db.execute(
        """SELECT f.film_id, f.title, l.name AS language FROM film f 
            JOIN language l ON l.language_id = f.language_id
            ORDER BY f.title ASC"""
    ).fetchall()
    return render_template('movies/index.html', movies=movies)

def get_movie(id):
    movie = get_db().execute(
        'SELECT * FROM film WHERE film_id == ?'(id),
    ).fetchone()

    return movie



@bp.route("/info/<int:id>/")
def info(id):
#     db = get_db()
#     movie_info = db.execute("""SELECT f.film_id, f.title, l.name
#                             f.rating, f.length, a.firts_name, a.last_name
#                             FROM film f JOIN language l ON f.language_id = f.language_id """)
     return str(id)
