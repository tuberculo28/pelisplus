from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from flaskr.db import get_db

bp = Blueprint('film', __name__)

@bp.route('/')
def index():
    db = get_db()
    movie = db.execute(
        'SELECT * FROM film ORDER BY film DESC'
    ).fetchall()
    return render_template('movies/index.html', movie=movie)

def get_movie(id):
    movie = get_db().execute(
        'SELECT * FROM film',
        (id,)
    ).fetchone()

    return movie