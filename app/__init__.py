from werkzeug.exceptions import HTTPException

from flask import Flask, jsonify
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///certificate_test_bot'
db = SQLAlchemy(app)

from app import views
api.add_namespace(views.certificate.certificate_ns)

@app.errorhandler(HTTPException)
def handler(e):
    return jsonify(message=e.description, status=e.code), e.code
