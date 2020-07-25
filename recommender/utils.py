import flask


class Utils(object):

    def method_get(self):
        return flask.render_template('index.html')

    def method_post(self):
        anime_name = flask.request.form['anime_name']
        tv_or_movie = flask.request.form['tv_or_movie']
        anime_name = anime_name.title()
        tv_movie = tv_or_movie.title()
        return anime_name, tv_movie
