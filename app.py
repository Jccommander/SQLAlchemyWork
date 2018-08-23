import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Set up the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Automap the base to reflect the database
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create references for each database table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create the session from python to the database
session = Session(engine)

# Set up Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/(startdate)<br>"
        f"/api/v1.0/(startdate-enddate)"
    )


@app.route("/api/v1.0/names")
def names():



@app.route("/api/v1.0/passengers")
def passengers():


if __name__ == '__main__':
    app.run(debug=True)