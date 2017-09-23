#!/usr/bin/python3
from models import storage
from flask import Flask
from flask import render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """calls close method of storage"""
    storage.close()


@app.route('/hbnb')
def hbnb():
    """hbnb method"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    places = storage.all("Place").values()
    users = storage.all("User").values()
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places, users=users)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
