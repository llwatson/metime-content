from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.Text(500), unique=False)

    def __init__(self, title, content):
      self.title = title
      self.content = content


class QuotesSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')


quote_schema = QuotesSchema()
quotes_schema = QuotesSchema(many=True)


@app.route('/quote', methods=["POST"])
def add_quote():
    title = request.json['title']
    content = request.json['content']

    new_quote = Quotes(title, content)

    db.session.add(new_quote)
    db.session.commit()

    quote = Quotes.query.get(new_quote.id)

    return quote_schema.jsonify(quote)

@app.route("/quotes", methods=["GET"])
def get_quotes():
      all_quotes = Quotes.query.all()
      result = quotes_schema.dump(all_quotes)
      return jsonify(result)


@app.route("/quote/<id>", methods=["GET"])
def get_quote(id):
    quote = Quotes.query.get(id)
    return quote_schema.jsonify(quote)



@app.route("/quote/<id>", methods=["PUT"])
def quote_update(id):
    quote = Quotes.query.get(id)
    title = request.json['title']
    content = request.json['content']

    quote.title = title
    quote.content = content

    db.session.commit()
    return quote_schema.jsonify(quote)
    

@app.route("/quote/<id>", methods=["DELETE"])
def quote_delete(id):
    quote = Quotes.query.get(id)
    db.session.delete(quote)
    db.session.commit()

    return quote_schema.jsonify(quote)
    


if __name__== '__main__':
    app.run(debug=True)