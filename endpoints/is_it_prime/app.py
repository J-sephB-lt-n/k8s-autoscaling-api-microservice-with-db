"""
docstring TODO
"""

import flask

app = flask.Flask(__name__)

@app.route("/<num>", methods=["GET"])
def is_it_prime(num: str):
    """docstring TODO"""
    num: int = int(num)
    return flask.Response(f"I don't know if {num} is prime or not", status=200)
