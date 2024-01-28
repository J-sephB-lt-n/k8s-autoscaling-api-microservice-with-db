"""
docstring TODO
"""

import flask

app = flask.Flask(__name__)

@app.route("/is_it_prime/<num>", methods=["GET"])
def is_it_prime(num: str):
    """docstring TODO"""
    num: int = int(num)
    return flask.Response("SERVICE UNAVAILABLE", status=502)
