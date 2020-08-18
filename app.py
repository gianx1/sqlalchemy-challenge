import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Hawaii.sqlite")
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurements = Base.classes.measurements

# Create our session (link) from Python to the DB
session = Session(engine)



# Flask Setup
app = Flask(__name__)

# List all the routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = dt.date(2017, 8 ,23)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temps = (session.query(Measurement.date, Measurement.prcp)
            .filter(Measurement.date <= last_date)
            .filter(Measurement.date >= year_ago)
            .order_by(Measurement.date).all())
             
    rain_fall = {date: prcp for date, prcp in temps}
             
    return jsonify(rain_fall)


@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.station).all()
    return jsonify(stations)


@app.route('/api/v1.0/tobs') 
def tobs():  
    last_date = dt.date(2017, 8 ,23)
    year_ago = maxDate - dt.timedelta(days=365)

    year = (session.query(Measurement.tobs)
                .filter(Measurement.station == 'USC00519281')
                .filter(Measurement.date <= maxDate)
                .filter(Measurement.date >= year_ago)
                .order_by(Measurement.tobs).all())
    
    return jsonify(year)


@app.route('/api/v1.0/<start>') 
def start(start=None):
    Tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())
    tobs_df = pd.DataFrame(Tobs)
    TAVG = tobs_df["tobs"].mean()
    TMAX = tobs_df["tobs"].max()
    TMIN = tobs_df["tobs"].min()
    
    return jsonify(TAVG, TMAX, TMIN)


@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):
    Tobs2 = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())
    tobs_df = pd.DataFrame(Tobs2)
    TAVG = tobs_df["tobs"].mean()
    TMAX = tobs_df["tobs"].max()
    TMIN = tobs_df["tobs"].min()
    
    return jsonify(TAVG, TMAX, TMIN)


if __name__ == '__main__':
    app.run(debug=True)