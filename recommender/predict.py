from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender.utils import Utils
import config as cfg

utils = Utils(cfg.read_cache, cfg.write_cache)


class Predict(object):
    def __init__(self, df, indices):
        self.df = df
        self.count = CountVectorizer(stop_words='english')
        self.count_matrix = self.count.fit_transform(self.df['comb_feat'])
        self.indices = indices

    def get_recommendations(self, title, tv_movie_input):
        cosine_sim = cosine_similarity(self.count_matrix, self.count_matrix)
        idx = self.indices[title]
        data = self.df[['title_english', 'type', 'score', 'anime_id']].copy()
        data['sim_score'] = cosine_sim[idx]
        data = utils.tv_or_movie(data, tv_movie_input)
        data = data.sort_values(['sim_score'], ascending=False)
        data = data[1:11]
        data = data[['title_english', 'score', 'anime_id']]
        data['anime_id'] = data['anime_id'].apply(lambda x: str("https://myanimelist.net/anime/") + str(x))
        data = data.rename(columns={'title_english': 'Title', 'score': 'Score', 'anime_id': 'Link'})
        return data
