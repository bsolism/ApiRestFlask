import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import numpy as np
from flask import Flask, jsonify
from numpy import nan
import json

app = Flask(__name__)


Df = pd.read_csv('netflix_titles.csv')

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(Df['listed_in'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indice = pd.Series(Df.index, index=Df['title']).drop_duplicates()


def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indice[title]
    sim_score = list(enumerate(cosine_sim[idx]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
    sim_score = sim_score[0:5]
    movie_indices = [i[0] for i in sim_score]
    resp = Df.iloc[movie_indices]
    return resp


titulo = str(Df.iloc[5]['title'])


@ app.route('/movie/<string:title>')
def get_movie(title):
    movie = get_recommendations(title)
    return movie.to_json(orient='records')


@ app.route('/movie')
def ping():
    return Df.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
