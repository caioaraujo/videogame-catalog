from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .models import Game
from videogame_catalog import db


bp = Blueprint('catalog', __name__)


@bp.route('/')
def index():
    games = Game.query.order_by(Game.name).all()
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
            game = Game(
                name=name,
                released_year=released_year,
                publisher=publisher,
                platform=platform,
                author_id=g.user.id,
            )
            db.session.add(game)
            db.session.commit()
            return redirect(url_for('catalog.index'))

    return render_template('catalog/create.html')


def get_game(id, check_author=True):
    game = Game.query.get(id)

    if game is None:
        abort(404, "Game id {0} doesn't exist.".format(id))

    if check_author and game.author_id != g.user.id:
        abort(403)

    return game


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    game = get_game(id)

    if request.method == 'POST':
        name = request.form['name']
        released_year = request.form['released_year']
        publisher = request.form['publisher']
        platform = request.form['platform']

        if not name:
            flash('Name is required.')
            return render_template('catalog/update.html', game=game)
        if not released_year:
            flash('Released year is required.')
            return render_template('catalog/update.html', game=game)
        if not publisher:
            flash('Publisher is required.')
            return render_template('catalog/update.html', game=game)
        if not platform:
            flash('Platform is required.')
            return render_template('catalog/update.html', game=game)

        game.name = name
        game.released_year = released_year
        game.publisher = publisher
        game.platform = platform
        db.session.add(game)
        db.session.commit()
        return redirect(url_for('catalog.index'))

    return render_template('catalog/update.html', game=game)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    game = get_game(id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('catalog.index'))
