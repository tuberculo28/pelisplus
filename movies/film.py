from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify

)
from werkzeug.exceptions import abort

from movies.db import get_db

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
def index_actor():
    db = get_db()
    actors = db.execute(
        'SELECT * FROM actor ORDER BY last_name, first_name ASC'
    ).fetchall()
    return render_template('actor/index.html', actors=actors)

def get_movie(id):
    movie = get_db().execute(
        """SELECT f.film_id, f.release_year, a.first_name as nombre, a.last_name as apellido, c.name as categoria 
                        FROM film f
                             JOIN film_category fc ON f.film_id = fc.film_id
                             JOIN category c ON fc.category_id = c.category_id
                             JOIN film_actor fa ON f.film_id = fa.film_id
                             JOIN actor a ON fa.actor_id = a.actor_id
                             WHERE f.film_id = ?""",(id,)
                             ).fetchone()

    return movie

def get_actors(id):
    actor = get_db().execute(
        """SELECT a.actor_id, f.film_id, a.first_name as nombre, a.last_name as apellido FROM film f
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN actor a ON fa.actor_id = a.actor_id
        WHERE f.film_id = ?""",(id,)
    ).fetchall()
    return actor

def get_categorias(id):
    categoria = get_db().execute(
        """SELECT f.film_id, c. name as categorias FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE f.film_id = ?""",(id,)
    ).fetchall()
    return categoria 

def get_idioma(id):
    idioma = get_db().execute(
        """SELECT f.film_id, l.name as idioma FROM film f
        JOIN language l ON f.language_id = l.language_id
        WHERE f.film_id = ?""",(id,)
    ).fetchone()
    return idioma

@bp.route("/info/<int:id>/")
def info(id):
    movie_info = get_movie(id)
    movie_actors = get_actors(id)
    movie_categories = get_categorias(id)
    movie_language = get_idioma(id)
    return render_template('movies/info.html', movie_info=movie_info, movie_actors=movie_actors,
                           movie_categories=movie_categories, movie_language=movie_language)

@bp.route("/artists/<int:id>/")
def artists(id):
#    artist_info =  get_artists_info(id)
    artist_movies = get_artists_movies(id)
    return render_template('movies/artists.html',  
                           artist_movies = artist_movies)

#def get_artists_info(id):
#    artist = get_db().execute(
#        """SELECT actor_id, first_name, last_name FROM actor""",(id,)).fetchone()
#    return artist

def get_artists_movies(id):
    artistas_pelis = get_db().execute(
        """SELECT f.film_id,a.actor_id, f.title as peli, a.first_name, a.last_name FROM film f
            JOIN film_actor fa ON f.film_id = fa.film_id
            JOIN actor a ON fa.actor_id = a.actor_id
            WHERE a.actor_id = ?""",(id,)).fetchall()
    return artistas_pelis

@bp.route("/api/movies")
def index_api():
    db = get_db()
    movies = db.execute(
        """SELECT f.film_id, f.title, l.name AS language FROM film f 
            JOIN language l ON l.language_id = f.language_id
            ORDER BY f.title ASC"""
    ).fetchall()

    for m in movies:
        m["url"] = url_for('film.info_api', id=m['film_id'], _external=True)

    return jsonify(movies)

@bp.route("/api/info/<int:id>/")
def info_api(id):
    movie_info = get_movie(id)
    movie_actors = get_actors(id)
    movie_categories = get_categorias(id)
    movie_language = get_idioma(id)

    for i in movie_info:
        i["url"] = url_for('film.get_artists_movies', id=i['actor_id'], _external=True)

    return jsonify(movie_info=movie_info, movie_actors=movie_actors,
                           movie_categories=movie_categories, movie_language=movie_language)