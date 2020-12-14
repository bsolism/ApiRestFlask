from flask import Flask, jsonify
from service import get_recommendations, Df

app = Flask(__name__)


@ app.route('/movie/<string:title>')
def get_movie(title):
    movie = get_recommendations(title)
    return movie.to_json(orient='records')


@ app.route('/movie')
def ping():
    return Df.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
