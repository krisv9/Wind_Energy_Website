from flask import Flask, render_template
import random
from datetime import datetime, timedelta

app = Flask(__name__)

STATIONS = {
    "overall": "Overall",
    "gemini": "Gemini",
    "borssele_12": "Borssele 1&2",
    "borssele_34": "Borssele 3&4",
    "hollandse_kust_zuid": "Hollandse Kust Zuid",
    "hollandse_kust_noord": "Hollandse Kust Noord",
}

def get_forecast_data(station):
    """
    Returns mock hourly forecast data for the given station.
    Replace the body of this function with a REST API call when ready.
    """
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    hours = [now + timedelta(hours=i) for i in range(24)]

    seed = sum(ord(c) for c in station)
    random.seed(seed)
    power_output = [round(random.uniform(50, 500), 2) for _ in hours]
    actual_output = [round(v + random.uniform(-30, 30), 2) for v in power_output]

    return {
        "labels": [h.strftime("%H:%M") for h in hours],
        "predicted": power_output,
        "actual": actual_output,
        "metrics": {
            "mae": round(random.uniform(20, 35), 1),
            "rmse": round(random.uniform(28, 45), 1),
            "r2": round(random.uniform(0.85, 0.95), 2),
        },
        "last_updated": now.strftime("%d %b %Y, %H:%M"),
        "data_source": "Placeholder (REST API not yet connected)",
        "station_name": STATIONS[station],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stations")
def stations():
    return render_template("stations.html", stations=STATIONS)


@app.route("/dashboard/<station>")
def dashboard(station):
    if station not in STATIONS:
        return "Station not found", 404
    data = get_forecast_data(station)
    return render_template("dashboard.html", data=data, station=station)


if __name__ == "__main__":
    app.run(debug=True)
