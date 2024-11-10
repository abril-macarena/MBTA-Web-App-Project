from flask import Flask, render_template, request, redirect, url_for
import mbta_helper 


app = Flask(__name__)

# # Example code that shows flask structure
# @app.route("/")
# def hello():
#     return "Hello World!"


# Home page with a form to enter a place name
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the place name from the form
        place_name = request.form.get("place_name")
        
        # If place_name is provided, redirect to nearest MBTA route with the place_name parameter
        if place_name:
            return redirect(url_for("nearest_mbta", place_name=place_name))
    
    # Render the index.html template for GET requests or if place_name is not provided
    return render_template("index.html")

# Route to show the nearest MBTA station based on place name
@app.route("/nearest_mbta")
def nearest_mbta():
    # Get the place name from the URL parameters
    place_name = request.args.get("place_name")
    
    # If place_name is missing, show an error message
    if not place_name:
        return redirect(url_for("error"))

    # Try to get the nearest station and accessibility info
    try:
        station_name, wheelchair_accessible = mbta_helper.find_stop_near(place_name)
        return render_template(
            "mbta_station.html",
            place_name=place_name,
            station_name=station_name,
            wheelchair_accessible=wheelchair_accessible,
        )
    except:
        # Redirect to an error page if an exception occurs
        return redirect(url_for("error"))

# Error page route
@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
