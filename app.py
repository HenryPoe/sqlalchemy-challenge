# App.py
# Henry Poe
# Last edited: 05/08/2021

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt


# Flask Set-up
app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Routes
#################################################

# Home Page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[Start-Date]<br/>"
        f"/api/v1.0/[Start-Date]/[End-Date]<br/>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all measurements date and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    # Create a dictionary 
    measurements = []
    for date, prcp in results:
        measurements_dict = {}
        measurements_dict["date"] = date
        measurements_dict["precipitation"] = prcp
        measurements.append(measurements_dict)
    
    # Return the json of dates and precipitations
    return jsonify(measurements)

# Stations route
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all stations
    results = session.query(Station.station).all()
    session.close()
    
    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Get the counts of measurments taken by station
    station_counts = session.query(Measurement.station, func.count()).\
    group_by(Measurement.station).\
    all()
    largestStation = max(station_counts, key=lambda x:x[1])
    
    # Starting from the most recent data point in the database. 
    mostRecent_str = engine.execute("SELECT MAX(date) FROM measurement").fetchall()[0][0]
    mostRecent_dt = dt.datetime.strptime(mostRecent_str, "%Y-%m-%d")
    # Calculate the date one year from the last date in data set.
    yearAgo_dt = mostRecent_dt.replace(year=mostRecent_dt.year-1)
    yearAgo_str = dt.datetime.strftime(yearAgo_dt, "%Y-%m-%d")
        
    results = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.station == f"{largestStation}", Measurement.date > f"{yearAgo_str}").all()
    session.close()
    
    # Create a dictionary 
    tobs_output = []
    for tobs, date in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["TOBS"] = tobs
        tobs_output.append(tobs_dict)
    
    # Return the json of dates and precipitations
    return jsonify(list(np.ravel(results)))

# Start date temperature info route
@app.route("/api/v1.0/<start>")
def from_date(start):
    print("Server received request for")
    return "a;lskfj;alskdjf;alsdkjf;aslkdfj;aslkfj"

# Start and End date temperature info route
@app.route("/api/v1.0/<start>/<end>")
def range_dates(start, end):
    print("Server received request for")
    return


if __name__ == "__main__":
    app.run(debug=True)
