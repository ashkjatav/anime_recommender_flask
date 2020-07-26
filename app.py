import flask
from recommender.prep import Prep
from recommender.utils import Utils
from recommender.predict import Predict
import config as cfg
import pandas as pd

app = flask.Flask(__name__, template_folder='templates')

utils = Utils(cfg.read_cache, cfg.write_cache)
prep = Prep(cfg.anime_list, utils.read_cache, utils.write_cache)


# Set up the main route
# TODO add an option to read cached preprocessed file
@app.route('/', methods=['GET', 'POST'])
def main():
    df = prep.read_data()
    if flask.request.method == 'GET':
        return utils.method_get()

    if flask.request.method == 'POST':
        anime_name, tv_movie = utils.method_post()
        df, indices, all_titles = prep.preprocess(df, tv_movie_input=tv_movie)
        if anime_name not in all_titles:
            return (flask.render_template('negative.html', name=anime_name))
        else:
            pred = Predict(df, indices)
            result_final = pred.get_recommendations(anime_name, tv_movie_input=tv_movie)
            names = result_final['Title'].values
            dates = result_final['Score'].values
            anime_id = result_final['Link'].values
            return flask.render_template('positive.html', movie_names=names, movie_date=dates,
                                         anime_id=anime_id, search_name=anime_name)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
