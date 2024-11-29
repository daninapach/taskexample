from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "cc7dca872ec2d82ad44d382a89ccabb8"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


@app.route("/")
def index():
    return render_template("index.html", unit="metric")


@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.form.get("city")
    unit = request.form.get("unit") or "metric"

    if not city:
        return render_template("index.html", error="Please enter a city name.", unit=unit)

    # Fetch weather data
    params = {"q": city, "appid": API_KEY, "units": unit}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize(),
            "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        return render_template("index.html", weather=weather, unit=unit)
    else:
        return render_template("index.html", error=f"City not found: {city}. Please try again.", unit=unit)


if __name__ == "__main__":
    app.run(debug=True)
