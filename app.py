from flask import Flask, render_template, request, redirect, url_for
import mbta_helper 


app = Flask(__name__)

# # Example code that shows flask structure
# @app.route("/")
# def hello():
#     return "Hello World!"


# Home page with a form allowing user to enter location
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place_name = request.form.get("place_name")
        if place_name:
            return redirect(url_for("nearest_mbta", place_name=place_name))
    
    return render_template("index.html")

# Page to show nearest MBTA station details
@app.route("/nearest_mbta")
def nearest_mbta():
    place_name = request.args.get("place_name")
    if not place_name:
        return redirect(url_for("error"))

    try:
        station_name, wheelchair_accessible = mbta_helper.find_stop_near(place_name)
        return render_template(
            "mbta_station.html",
            place_name=place_name,
            station_name=station_name,
            wheelchair_accessible=wheelchair_accessible,
        )
    except:
        return redirect(url_for("error")) #redirects to error page if needed

# Error page 
@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
