"""
docstring TODO
"""
# standard lib imports #
import json

# 3rd party imports #
import flask
import psycopg

app = flask.Flask(__name__)


@app.route("/query", methods=["POST"])
def query():
    """docstring TODO"""
    user_input_json: dict[str, str] = flask.request.get_json()
    db_name: str = user_input_json["db_name"]
    query_string: str = user_input_json["query_string"]
    with psycopg.connect(
        f"host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='{db_name}' user='db_admin' password='password1234' connect_timeout=10",
        autocommit=True,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(query_string)
            try:
                results = cur.fetchall()
            except psycopg.ProgrammingError:
                results = None
        return flask.Response(
            json.dumps(
                {
                    "results": results,
                    "description": None
                    if cur.description is None
                    else [str(x) for x in cur.description],
                    "statusmessage": cur.statusmessage,
                    "rowcount": cur.rowcount,
                }
            ),
            status=200,
        )
    return flask.Response("BAD REQUEST", status=400)
