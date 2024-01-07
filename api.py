from flask import Flask

from mongo.mongo import mongo

app = Flask(__name__)

@app.route("/")
def ping_route():
    return "i'm alive"

@app.route("/version")
def version_route():
    mongo_version = mongo.getVersion()
    return {"version": mongo_version}

@app.route("/medicine/<string:cis>") # 61266250
def get_medicines_route(cis):
    medicine = mongo.getMedicineByCis(cis)

    if medicine is None:
        return {"error": "no medicine found with this cis"}, 404
    return medicine


def start_api():
    app.run(host="localhost", port=8080)
