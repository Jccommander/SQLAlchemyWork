import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

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
        f"/api/v1.0/(startdate)/(enddate)"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculation for the last year of the dataset
    year_ago = dt.datetime.now() - dt.timedelta(365)
    two_years_ago = year_ago - dt.timedelta(365)

    # Query for the SQL database, retreiving date and prcp within the date range
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date < year_ago)\
    .filter(Measurement.date > two_years_ago).all()

    all_dates = []

    for result in results:
        percip_dict = {}
        percip_dict['date'] = result.date
        percip_dict['rainfall'] = result.prcp
        all_dates.append(percip_dict)
    
    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station, Station.name, Station.latitude, Station.longitude,\
    Station.elevation).all()

    station_list = []
    for station in stations:
        station_dict = {}
        station_dict['station_id'] = station.station
        station_dict['name'] = station.name
        station_dict['latitude'] = station.latitude
        station_dict['longitude'] = station.longitude
        station_dict['elevation'] = station.elevation
        station_list.append(station_dict)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tempobs():
    year_ago = dt.datetime.now() - dt.timedelta(365)
    two_years_ago = year_ago - dt.timedelta(365)

    tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date < year_ago)\
    .filter(Measurement.date > two_years_ago).filter(Measurement.station == 'USC00519281').all()

    temperature_list = []
    for obs in tobs:
        temp_dict = {}
        temp_dict['date'] = obs.date
        temp_dict['temp'] = obs.tobs
        temperature_list.append(temp_dict)

    return jsonify(temperature_list)


@app.route("/api/v1.0/<start_date>")
def start_temperature(start_date):
    request = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
    func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    temp_dict = {}
    temp_dict['date'] = start_date
    temp_dict['min'] = request[0][0]
    temp_dict['avg'] = request[0][1]
    temp_dict['max'] = request[0][2]

    if temp_dict:
        return jsonify(temp_dict)

    return jsonify({"error": f"The date entered: {start_date} was invalid or not found."}), 404


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_temperature(start_date, end_date):
    request = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
    func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter\
    (Measurement.date <= end_date).all()

    temp_dict = {}
    temp_dict['start_date'] = start_date
    temp_dict['end_date'] = end_date
    temp_dict['min'] = request[0][0]
    temp_dict['avg'] = request[0][1]
    temp_dict['max'] = request[0][2]

    if temp_dict:
        return jsonify(temp_dict)

    return jsonify({"error": f"The dates entered: {start_date}, {end_date} were invalid or not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)