# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 23:01:32 2019

@author: xiang
"""

import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#creating engine for connecting with hawaii sqlite database

engine = create_engine("sqlite:///Hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
print(Base.classes.keys())

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    print('Hawaii')
    return (
        f"Hawaii weather info app<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
   
    )


@app.route("/api/v1.0/station")
def stations():
    """Return a list of all stations from the dataset"""
    # Query all passengers
    station = session.query(Station.station).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(station))

    return jsonify(station_names)


@app.route("/api/v1.0/prcp")
def prcp():
    """Return a list of last 12 months precipitation data from sqlite dataset"""
    # Query all prcp data
    
    last_year =dt.date.today()-dt.timedelta(days=1000)
    prcp_results = session.query(Measurement.date,Measurement.prcp).\
                   filter(Measurement.date >= last_year).\
                   all()
    
    #Create a dictionary from the row data and append to a list of all_prcp
    #prcp_dict = dict(prcp_results)
    
    all_prcp = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all tobs from the dataset"""
    last_year =dt.date.today()-dt.timedelta(days=1000)
    tobs_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                   filter(Measurement.date >= last_year).all()
    
    
    # Create a list from the row data and append to a list of all_tobs
    tobslist = list(np.ravel(tobs_results))

    return jsonify(tobslist)

@app.route("/api/v1.0/start")
def start():
    """Return a list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # Query min, avg, max tob value
    start_date = dt.date(2017,5,1)-dt.timedelta(days=365)
    start_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                   filter(Measurement.date >= start_date).all()
    # Convert list of tuples into json file
    
    return jsonify(start_results)

@app.route("/api/v1.0/start_end")
def start_end():
    """Return a list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # Query min, avg, max tob value
    start_date = dt.date(2015,5,1)-dt.timedelta(days=365) 
    end_date = dt.date(2016,5,1)-dt.timedelta(days=365)
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

   
    return jsonify(start_end_results)


if __name__ == '__main__':
      app.run(host='127.0.0.1', port=81)