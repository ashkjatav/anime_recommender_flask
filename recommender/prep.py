import re, string
import os
from nltk import SnowballStemmer
import pandas as pd
import ast
import pickle
import numpy as np
from nltk import SnowballStemmer
from nltk.corpus import stopwords

stemmer = SnowballStemmer("english")

i = stopwords.words('english')
j = list(string.punctuation)
my_stopwords = ['written', 'by', 'mal', 'rewrit', 'source', 'ann']
stopwords = set(i).union(j, my_stopwords)


class Prep(object):
    def __init__(self, anime_pickle, read_cache, write_cache):
        self.anime_pickle = anime_pickle
        self.read_cache = read_cache
        self.write_cache = write_cache

    def read_data(self):
        if self.read_cache:
            animes = pd.read_csv("./data/anime_any.csv")
        else:
            with open(os.path.join("./data", self.anime_pickle), 'rb') as f:
                animes = pickle.load(f)
                animes = pd.DataFrame(animes.values())
        return animes

    def preprocess(self, df, tv_movie_input):
        # df[['producer', 'licensor', 'studio', 'genre', 'opening_theme', 'ending_theme']] = df[
        #     ['producer', 'licensor', 'studio', 'genre', 'opening_theme', 'ending_theme']].applymap(
        #     lambda x: ast.literal_eval(x))  #
        if self.read_cache:
            df = df  # self.tv_or_movie(df, tv_movie_input)
        else:

            df['genre_list'] = df['genre'].apply(lambda x: [name['name'] for name in x])
            df['producer_list'] = df['producer'].apply(lambda x: [name['name'] for name in x])
            df['title_english'] = np.where(df['title_english'].isnull(), df['title'], df['title_english'])
            df = self.tv_or_movie(df, tv_movie_input)
            cols = ['anime_id', 'title', 'title_english', 'type', 'score', 'genre_list', 'producer_list',
                    'opening_theme', 'ending_theme',
                    'synopsis', 'related']
            df = df[cols]
            df['comb_feat'] = df['genre_list'] + df['producer_list'] + df['opening_theme'] + df[
                'ending_theme'] + df[
                                  'synopsis'].apply(lambda x: x.split())
            df['comb_feat'] = df['comb_feat'].apply(lambda x: ' '.join(x))
            df = df.reset_index()
            df['comb_feat'] = df['comb_feat'].apply(self.preprocess_text)
        indices = pd.Series(df.index, index=df['title_english'])
        all_titles = df['title_english'].values
        df = df[['index', 'anime_id', 'title_english', 'type', 'score', 'comb_feat']]
        return df, indices, all_titles

    def tv_or_movie(self, df, tv_movie_input='Any'):
        if tv_movie_input == 'TV':
            return df[df['type'] == 'TV']
        elif tv_movie_input == 'Movie':
            return df[df['type'] == 'Movie']
        elif tv_movie_input == 'Any':
            return df

    def preprocess_text(self, x):
        stemmer = SnowballStemmer("english")
        x = re.sub('[^a-z\s]', ' ', x.lower())  # Removing noise from Description
        x = [stemmer.stem(w) for w in x.split() if
             stemmer.stem(w) not in set(stopwords)]  # Removing words not in list of stopwords
        x = [y for y in x if len(y) > 2]  # Removing words with length less than 2 characters.
        x = list(set(x))
        return ' '.join(x)
