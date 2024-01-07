import logging
import os

from flask import Flask

from mongo.mongo import Mongo

app = Flask(__name__)
app.logger.setLevel(logging.ERROR)

@app.route("/")
def ping_route():
    return "i'm alive"

@app.route("/version")
def version_route():
    mongo = Mongo(
        host=os.getenv("MONGO_HOST"),
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_PASSWORD")
    )
    mongo_version = mongo.getVersion()
    return {"version": mongo_version}

@app.route("/medicine/<string:cis>") # 61266250
def get_medicines_route(cis):
    mongo = Mongo(
        host=os.getenv("MONGO_HOST"),
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_PASSWORD")
    )
    medicine = mongo.getMedicineByCis(cis)

    if medicine is None:
        return {"error": "no medicine found with this cis"}, 404
    return medicine


def start_api():
    app.run(host="0.0.0.0", port=8080)
