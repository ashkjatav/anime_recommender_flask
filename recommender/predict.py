from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class Predict(object):
    def __init__(self, df, indices):
        self.df = df
        self.count = CountVectorizer(stop_words='english')
        self.count_matrix = self.count.fit_transform(self.df['comb_feat'])
        self.indices = indices

    def get_recommendations(self, title):
        cosine_sim = cosine_similarity(self.count_matrix, self.count_matrix)
        idx = self.indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [i[0] for i in sim_scores]
        tit = self.df['title_english'].iloc[movie_indices]
        # genre_list = df_tv['genre_list'].iloc[movie_indices]
        scor = self.df['score'].iloc[movie_indices]
        return_df = pd.DataFrame(columns=['Title', 'Score'])
        return_df['Title'] = tit
        # return_df['Genre'] = genre_list
        return_df['Score'] = scor
        return return_df
