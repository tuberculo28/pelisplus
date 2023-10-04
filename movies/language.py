from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from flaskr.db import get_db

bp = Blueprint('language', __name__)

@bp.route('/language')
def index():
    db = get_db()
    language = db.execute(
        'SELECT * FROM language ORDER BY name ASC'
    ).fetchall()
    return render_template('movies/info.html', language=language)