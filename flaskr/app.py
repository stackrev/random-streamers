from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
    jsonify,
)
import os
import random
import json
import string
from time import sleep
from datetime import datetime, date, timedelta


def random_date(year_start=2000, year_end=2005):
    """Random datetime between 2 dates"""
    start_date = datetime(year_start, 1, 1)
    end_date = datetime(year_end, 1, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_seconds = random.randrange(0, 60 * 60 * 24)
    rand_date = start_date + timedelta(
        days=random_number_of_days, seconds=random_seconds
    )

    return rand_date


def random_data(include_digits=False, include_nulls=False):
    """Generate a random string of fixed length"""
    size = random.randint(10, 200)
    if include_nulls and bool(random.getrandbits(1)):
        rand_str = None
    elif include_digits:
        rand_str = "".join(
            random.choice(string.ascii_letters + string.digits) for i in range(1, size)
        )
    else:
        rand_str = "".join(random.choice(string.ascii_letters) for i in range(1, size))
    return rand_str


def generate(include_digits=False, include_nulls=False):
    """create and return data in small parts"""
    for counter in range(1, 60):
        obj = dict()
        obj["id"] = counter
        obj["date"] = random_date().strftime("%m/%d/%Y, %H:%M:%S %p")
        obj["payload"] = random_data(include_digits, include_nulls)
        json_obj = json.dumps(obj)
        # sleep(1000)

        yield json_obj


def create_app(config=None):
    template_dir = os.path.relpath("./templates")
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir)
    app.config.from_object(__name__)
    if config is not None:
        app.config.update(config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.after_request
    def set_response_headers(response):
        """Ensures no cache"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.route("/stream1", methods=["GET"])
    def gimme_data1():
        """streams down large data"""

        # stream with context so the 'after_request' happens when streaming is finished
        return Response(stream_with_context(generate()), mimetype="application/json")

    @app.route("/stream2", methods=["GET"])
    def gimme_data2():
        """streams down large data"""

        # stream with context so the 'after_request' happens when streaming is finished
        return Response(
            stream_with_context(generate(include_digits=True)),
            mimetype="application/json",
        )

    @app.route("/stream3", methods=["GET"])
    def gimme_data3():
        """streams down large data"""

        # stream with context so the 'after_request' happens when streaming is finished
        return Response(
            stream_with_context(generate(include_digits=True, include_nulls=True)),
            mimetype="application/json",
        )

    @app.route("/")
    def entry_point():
        """simple entry for test"""

        return render_template("base.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
