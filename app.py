import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import and_
from flask import Flask, jsonify

# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
meas = Base.classes.measurement
station = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)

#Welcome Page
@app.route("/")
def welcome():
    print("Server received request for 'Home' page...")
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
###############################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'percipitation' page")
    session = Session(engine)

    results = session.query(meas.date, meas.prcp).all()
    session.close

    

    dates = []
    for date, prcp in results:
        dates_dict = {}
        dates_dict["date"] = date
        dates_dict["prcp"] = prcp
        dates.append(dates_dict)

  

    return jsonify(dates)

##############################################################
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page")
    session = Session(engine)

    results = session.query(station.station).all()

    session.close
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

##############################################################
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page")
    session = Session(engine)

    results = session.query(meas.date, meas.tobs).\
        filter(meas.date >= "2016-08-23").\
            filter(meas.station == "USC00519281").\
                order_by(meas.date).all()

    session.close

    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

##############################################################
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'start date' page")
    session = Session(engine)

    results = session.query(meas.date).all()
    all_dates = list(np.ravel(results))
    for date in all_dates:
        #print(date)
        if date == start:
            results2 = session.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
                filter(meas.date >= start).all()
            

   
            all_stats = []
            for min, max,avg in results2:
                stats_dict = {}
                stats_dict["min_temp"] = min
                stats_dict["max_temp"] = max
                stats_dict["avg_temp"] = round(avg,2)
                all_stats.append(stats_dict)
    
            return jsonify(all_stats)
    session.close
    

    return jsonify({"error": "Date not found. Use correct format: YYYY-MM-DD"}), 404
##############################################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    print("Server received request for 'start date to end date' page")
    session = Session(engine)
    results = session.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
                filter(and_(meas.date >= start, meas.date <= end)).all()
    

    session.close
    all_stats = []
    for min, max,avg in results:
        stats_dict = {}
        stats_dict["min_temp"] = min
        stats_dict["max_temp"] = max
        stats_dict["avg_temp"] = round(avg,2)
        all_stats.append(stats_dict)
        return jsonify(all_stats)
    return(start":"end)
                
   



if __name__ == '__main__':
    app.run(debug=True)