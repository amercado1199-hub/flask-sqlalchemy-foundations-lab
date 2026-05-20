#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

    if Earthquake.query.count() == 0:
        db.session.add(Earthquake(magnitude=9.5, location="Chile", year=1960))
        db.session.add(Earthquake(magnitude=9.2, location="Alaska", year=1964))
        db.session.add(Earthquake(magnitude=8.6, location="Alaska", year=1946))
        db.session.add(Earthquake(magnitude=8.5, location="Banda Sea", year=1934))
        db.session.add(Earthquake(magnitude=8.4, location="Chile", year=1922))
        db.session.commit()

@app.route("/")
def home():
    return "<h1>Earthquake API</h1>"


@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):

    quake = Earthquake.query.filter_by(id=id).first()

    if quake:
        return jsonify({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }), 200

    return jsonify({
        "message": f"Earthquake {id} not found."
    }), 404


@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_by_magnitude(magnitude):

    quakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    return jsonify({
        "count": len(quakes),
        "quakes": [
            {

                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            }
            for quake in quakes
        ]
    }), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)

