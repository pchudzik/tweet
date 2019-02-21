from flask import Flask, jsonify, request
from collections import namedtuple

import users


def create_app(debug=True):
    app = Flask(__name__)
    app.debug = True
    return app


app = create_app()

Message = namedtuple("Message", "from_, message")


@app.route("/users", methods=["POST"])
def add_user():
    payload = request.get_json()
    user = users.create_user(payload.get("name"), payload.get("password"))
    return jsonify(user._asdict())


if __name__ == "__main__":
    app.run()
