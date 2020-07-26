import pickle

import flask


class Utils(object):
    def __init__(self, read_cache, write_cache):
        self.read_cache = read_cache
        self.write_cache = write_cache

    def method_get(self):
        return flask.render_template('index.html')

    def method_post(self):
        anime_name = flask.request.form['anime_name']
        tv_or_movie = flask.request.form['type']
        return anime_name, tv_or_movie

    def tv_or_movie(self, df, tv_movie_input='Any'):
        if tv_movie_input == 'TV':
            return df[df['type'] == 'TV']
        elif tv_movie_input == 'Movie':
            return df[df['type'] == 'Movie']
        elif tv_movie_input == 'Any':
            return df
