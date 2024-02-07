from flask import Flask, render_template, jsonify
from database.db_functions import get_records_special
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/devices/')
def devices():
    devices_dict = get_records_special("devices")
    for device in devices_dict:
        pets_list = json.loads(device["pets"])
        pets_dict = {str(pet["id"]): pet["name"] for pet in pets_list}
        device["pets"] = pets_dict
    return render_template("devices.html", data=devices_dict)


@app.route('/pets/')
def pets():
    pets_dict = get_records_special("pets")
    for pet in pets_dict:
        devices_list = json.loads(pet["devices"])
        devices_dict = {str(device["id"]): device["name"] for device in devices_list}
        pet["devices"] = devices_dict
    return render_template("pets.html", data=pets_dict)


@app.route('/history/')
def history():
    history_list = get_records_special("history")
    return jsonify(history_list)


@app.route('/pets/add_form/')
def add_pet():
    return render_template("pet_form.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
