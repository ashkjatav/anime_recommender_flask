import flask
from recommender.prep import Prep
from recommender.utils import Utils
from recommender.predict import Predict

app = flask.Flask(__name__, template_folder='templates')

prep = Prep("data/AnimeList.pickle")
utils = Utils()


# Set up the main route
# TODO add an option to read cached preprocess file
@app.route('/', methods=['GET', 'POST'])
def main():
    df = prep.read_pickle()
    if flask.request.method == 'GET':
        return utils.method_get()

    if flask.request.method == 'POST':
        anime_name, tv_movie = utils.method_post()
        df, indices, all_titles = prep.preprocess(df)
        pred = Predict(df, indices)
        result_final = pred.get_recommendations(anime_name)
        names = []
        dates = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])
            dates.append(result_final.iloc[i][1])

        return flask.render_template('positive.html', movie_names=names, movie_date=dates, search_name=anime_name)


if __name__ == '__main__':
    app.run()
