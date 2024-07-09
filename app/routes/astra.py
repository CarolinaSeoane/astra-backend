from flask import Blueprint, jsonify
from dummy_data.populate_db import Populate

astra = Blueprint("astra", __name__)

@astra.route("/populate")
def populate_db():
    print("Populating astra database")
    service = Populate()
    service.populate()
    return jsonify(), 200
