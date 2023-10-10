#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Set initial value of session['page_views'] to 0 if it's the first request
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views for every request
    session['page_views'] += 1

    # Fetch articles from the database 
    articles = Article.query.all()

    # Check page_views and return response accordingly
    if session['page_views'] <= 3:
        serialized_articles = [article.to_dict() for article in articles]
        return jsonify({'articles': serialized_articles})
    else:
        return make_response(jsonify({'message': 'Maximum pageview limit reached'}), 401)

@app.route('/articles/<int:id>')
def show_article(id):
    # Set initial value of session['page_views'] to 0 if it's the first request
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views for every request
    session['page_views'] += 1

    # Fetch article from the database 
    article = Article.query.get(id)

    # Check page_views and return response accordingly
    if session['page_views'] <= 3:
        if article:
            return jsonify(article.to_dict())
        else:
            return jsonify({'message': 'Article not found'}), 404
    else:
        return make_response(jsonify({'message': 'Maximum pageview limit reached'}), 401)

if __name__ == '__main__':
    app.run(port=5555)

