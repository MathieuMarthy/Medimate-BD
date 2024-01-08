import logging

from flask import Flask

from mongo.mongo import mongo

app = Flask(__name__)
app.logger.setLevel(logging.ERROR)


@app.route("/")
def ping_route():
    return "i'm alive"


@app.route("/version")
def version_route():
    version, updated_documents_cis = mongo.getVersion()
    return {
        "version": version,
        "updated_documents_cis": updated_documents_cis
    }

@app.route("/version/<int:clientVersion>")
def get_diff_between_versions_route(clientVersion):
    if not isinstance(clientVersion, int) or clientVersion < 0:
        return None, 400

    codes_cis = mongo.getChangesBetweenClientVersion(clientVersion)
    return codes_cis


@app.route("/medicine/<int:cis>")
def get_medicines_route(cis):
    if not isinstance(cis, int):
        return None, 400

    medicine = mongo.getMedicineByCis(cis)

    if medicine is None:
        return {"error": "no medicine found with this cis"}, 404
    return medicine


def start_api():
    app.run(host="0.0.0.0", port=8080)
