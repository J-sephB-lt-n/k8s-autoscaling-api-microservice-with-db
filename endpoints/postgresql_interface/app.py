"""
docstring TODO
"""

import flask

app = flask.Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    """docstring TODO"""
    query_string: str = flask.request.get_json()["query_string"]
    return flask.Response(f"Received PostgreSQL query '{query_string}'", status=200)
