from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db


bp = Blueprint('catalog', __name__)


@bp.route('/')
def index():
    db = get_db()
    games = db.execute(
        'SELECT g.id, name, publisher, released_year,'
        ' platform, created, author_id, username'
        ' FROM game g JOIN user u ON g.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('catalog/index.html', games=games)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        released_year = request.form['released_year']
        publisher = request.form['publisher']
        platform = request.form['platform']

        if not name:
            flash('Name is required.')
        elif not released_year:
            flash('Released year is required.')
        elif not publisher:
            flash('Publisher is required.')
        elif not platform:
            flash('Platform is required.')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO game (name, released_year,'
                ' publisher, platform, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (name, released_year, publisher, platform, g.user['id'])
            )
            db.commit()
            return redirect(url_for('catalog.index'))

    return render_template('catalog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT g.id, name, released_year, publisher,'
        ' platform, created, author_id, username'
        ' FROM game g JOIN user u ON g.author_id = u.id'
        ' WHERE g.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Game id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    game = get_post(id)

    if request.method == 'POST':
        name = request.form['name']
        released_year = request.form['released_year']
        publisher = request.form['publisher']
        platform = request.form['platform']

        if not name:
            flash('Name is required.')
        elif not released_year:
            flash('Released year is required.')
        elif not publisher:
            flash('Publisher is required.')
        elif not platform:
            flash('Platform is required.')
        else:
            db = get_db()
            db.execute(
                'UPDATE game SET name = ?, released_year = ?,'
                ' publisher = ?, platform = ?'
                ' WHERE id = ?',
                (name, released_year, publisher, platform, id)
            )
            db.commit()
            return redirect(url_for('catalog.index'))

    return render_template('catalog/update.html', game=game)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM game WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('catalog.index'))
