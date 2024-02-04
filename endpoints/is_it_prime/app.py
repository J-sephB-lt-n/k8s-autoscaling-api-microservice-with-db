"""
Defines the /is_it_prime endpoint
"""

# standard lib imports #
import json
import time

# 3rd party imports #
import flask

# project module imports #
import prime_numbers

app = flask.Flask(__name__)


@app.route("/is_it_prime", methods=["GET"])
def is_it_prime():
    """Endpoint which determines whether a given number is a prime number or not
    Example response body:
    {
        "number": 69,
        "is_prime": false,
        "calc_time_secs": 0.04
    }
    """
    num: int = int(flask.request.args["num"])
    start_time: float = time.perf_counter()
    return flask.Response(
            json.dumps({"number": num, "is_prime": prime_numbers.is_prime(num), "calc_time_secs":f"{(time.perf_counter()-start_time):.2f}"}), status=200
    )
