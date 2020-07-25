import re, string
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
    def __init__(self, anime_pickle):
        self.dataFile = anime_pickle

    def read_pickle(self):
        with open(self.dataFile, 'rb') as f:
            animes = pickle.load(f)
            animes = pd.DataFrame(animes.values())
        return animes

    def preprocess(self, df, tv_movie_input='Any'):
        # df[['producer', 'licensor', 'studio', 'genre', 'opening_theme', 'ending_theme']] = df[
        #     ['producer', 'licensor', 'studio', 'genre', 'opening_theme', 'ending_theme']].applymap(
        #     lambda x: ast.literal_eval(x))  #
        df['genre_list'] = df['genre'].apply(lambda x: [name['name'] for name in x])
        df['producer_list'] = df['producer'].apply(lambda x: [name['name'] for name in x])
        df['title_english'] = np.where(df['title_english'].isnull(), df['title'], df['title_english'])

        df = self.tv_or_movie(df, tv_movie_input)

        cols = ['title', 'title_english', 'score', 'genre_list', 'producer_list', 'opening_theme', 'ending_theme',
                'synopsis', 'related']
        df = df[cols]
        # df_tv['title_english'] = np.where(df_tv['title_english'].isnull(), df_tv['title'], df_tv['title_english'])
        df['comb_feat'] = df['genre_list'] + df['producer_list'] + df['opening_theme'] + df[
            'ending_theme'] + df[
                              'synopsis'].apply(lambda x: x.split())
        df['comb_feat'] = df['comb_feat'].apply(lambda x: ' '.join(x))
        df = df.reset_index()
        indices = pd.Series(df.index, index=df['title_english'])
        all_titles = [df['title_english'][i] for i in range(len(df['title_english']))]
        df['comb_feat'] = df['comb_feat'].apply(self.preprocess_text)
        return df, indices, all_titles

    def tv_or_movie(self, df, tv_movie_input='Any'):
        if tv_movie_input == 'TV':
            return df[df['type'] != 'Movie']
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
