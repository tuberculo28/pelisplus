from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from movies.db import get_db

bp = Blueprint('actor', __name__, url_prefix="/actor/")
bpapi = Blueprint('api_actor', __name__, url_prefix="/api/actor/")

@bp.route('/')
def index():
    db = get_db()
    actors = db.execute(
        'SELECT * FROM actor ORDER BY last_name, first_name ASC'
    ).fetchall()
    return render_template('actor/index.html', actors=actors)

@bpapi.route('/')
def api_index():
    db = get_db()
    actors = db.execute(
        'SELECT * FROM actor ORDER BY last_name, first_name ASC'
    ).fetchall()
    return jsonify(actors=actors)
