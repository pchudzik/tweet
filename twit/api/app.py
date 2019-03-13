from flask import jsonify, Flask
from sqlalchemy.orm.exc import NoResultFound

from twit.api.followers import init_followers_endpoints
from twit.api.security import init_security
from twit.api.tweets import init_tweets_endpoints
from twit.api.users import init_users_endpoints
from twit.config import configuration
from twit.infrastructure import init_extensions
from twit.tokens import SecurityException


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = configuration.get("database", "url")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = configuration.get("database", "tack_modifications")
    app.config['JWT_SECRET_KEY'] = configuration.get("jwt", "secret")
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    init_extensions(app)
    init(app)
    return app


def init(app):
    init_security(app)
    init_users_endpoints(app)
    init_tweets_endpoints(app)
    init_followers_endpoints(app)


app = create_app()


@app.errorhandler(NoResultFound)
def no_result_found_handler(error):
    return jsonify(message="not found", err=str(error)), 404


@app.errorhandler(SecurityException)
def security_exception_handler(error):
    return jsonify(message="Forbidden"), 403


@app.errorhandler(Exception)
def any_error_handler(error):
    print(str(error))
    return jsonify(message="not found", err=str(error)), 500
