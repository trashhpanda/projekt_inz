import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
import database.db_functions as db
import raspberry
import json
from datetime import datetime
import threading
from raspberry import scan, scan_event, open_lid, close_lid, add_event, lid_opened_event

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

events = {
    "scan": scan_event,
    "lid_opened": lid_opened_event,
}


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/devices/')
def devices():
    devices_dict = db.get_records_special("devices")
    for device in devices_dict:
        pets_list = json.loads(device["pets"])
        pets_dict = {str(pet["id"]): pet["name"] for pet in pets_list}
        device["pets"] = pets_dict

    return render_template("devices.html", data=devices_dict)


@app.route('/pets/')
def pets():
    pets_dict = db.get_records_special("pets")
    for pet in pets_dict:
        devices_list = json.loads(pet["devices"])
        devices_dict = {str(device["id"]): device["name"] for device in devices_list}
        pet["devices"] = devices_dict

    return render_template("pets.html", data=pets_dict)


@app.route('/history/')
def history():
    history_dict = db.get_records_special("history")
    return render_template("history.html", data=history_dict)


@app.route('/pets/add/', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        try:
            name = str(request.form['pet-name'])
            rfid = str(request.form['pet-rfid'])
            filename = 'cat.png'

            if 'pet-picture' in request.files:
                picture = request.files['pet-picture']
                if picture.filename != '':
                    ext = os.path.splitext(picture.filename)[1]
                    now = datetime.now().strftime('_%Y-%m-%d_%H:%M')
                    pic = str(name) + now + ext
                    filename = secure_filename(pic)
                    picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            pet_dict = {
                "name": name,
                "rfid": rfid,
                "photo": filename
            }

            db.add_pet(pet_dict)
        except Exception as e:
            print(e)

    return render_template("pet_form.html")


@app.route('/scan_rfid/')
def scan_rfid():
    rfid = scan()
    return str(rfid)


@app.route('/set_event/<event>/')
def set_event(event):
    ev = events[event]
    ev.set()
    return 'Event ' + event + ' set'


@app.route('/clear_event/<event>/')
def clear_event(event):
    ev = events[event]
    ev.clear()
    print(ev.is_set())
    return 'Event ' + event + ' cleared'


@app.route('/devices/add/', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        try:
            name = str(request.form['device-name'])
            description = str(request.form['device-desc'])

            device_dict = {
                "name": name,
                "description": description
            }

            print(device_dict)

            db.add_device(device_dict)
        except Exception as e:
            print(e)
    return render_template("device_form.html")


@app.route('/access/<pet_id>/<device_id>/remove/')
def remove_access(pet_id, device_id):
    db.remove_access(pet_id, device_id)
    return 'Access to device ' + device_id + ' removed for pet ' + pet_id + '.'


@app.route('/access/<pet_id>/<device_id>/')
def add_access(pet_id, device_id):
    db.add_access(pet_id, device_id)
    return 'Access to device ' + device_id + ' added for pet ' + pet_id + '.'


@app.route('/pet_names/<device_id>/')
def get_pet_names(device_id):
    pet_names = db.get_pet_names(device_id)
    return jsonify(pet_names)


@app.route('/device_names/<pet_id>/')
def get_device_names(pet_id):
    device_names = db.get_device_names(pet_id)
    return jsonify(device_names)


@app.route('/records/<table>/')
def display(table):
    data = db.get_records(table)
    return jsonify(data)


@app.route('/open/')
def open_device():
    open_lid()
    add_event('0', '1', 'OPEN')
    return 'lid opened manually'


@app.route('/close/')
def close_device():
    close_lid()
    add_event('0', '1', 'CLOSE')
    return 'lid closed manually'


@app.route('/lid_status/')
def check_lid_status():
    if lid_opened_event.is_set():
        return 'OPENED'
    else:
        return 'CLOSED'


def app_run():
    app.run(host='192.168.14.76')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
