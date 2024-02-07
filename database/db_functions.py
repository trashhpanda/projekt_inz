import os
import sqlite3
from datetime import datetime


def connect():
    """
    Connects to database.
    """
    here = os.path.dirname(os.path.abspath(__file__))

    database = os.path.join(here, "database.db")

    try:
        conn = sqlite3.connect(database)
        print("connected")
        cur = conn.cursor()
        return conn, cur
    except sqlite3.Error as e:
        print(e)


def commit_close(conn):
    """
    Commits changes and closes connection with database.
    """
    conn.commit()
    conn.close()


def create_tables():
    """
    Creates all tables for the database.
    """
    conn, cur = connect()

    queries = [
        '''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rfid TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            photo_filename TEXT NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS access (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            device_id INTEGER,
            FOREIGN KEY (pet_id) REFERENCES pets (id) ON DELETE CASCADE,
            FOREIGN KEY (device_id) REFERENCES devices (id) ON DELETE CASCADE
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime DATETIME,
            pet_id INTEGER,
            device_id INTEGER,
            event TEXT NOT NULL,
            FOREIGN KEY (device_id) REFERENCES devices (id),
            FOREIGN KEY (pet_id) REFERENCES pets (id)
        );
        '''
    ]

    for query in queries:
        cur.execute(query)

    commit_close(conn)


def get_records(table_name):
    """
    Lists all records in a specified table.
    """
    query = 'SELECT * FROM ' + table_name + ';'

    conn, cur = connect()

    rows = []

    try:
        cur.execute(query)
        rows = cur.fetchall()
    except sqlite3.IntegrityError as e:
        print("Error: ", e)

    commit_close(conn)

    return rows if rows else None


def delete_record_by_id(table_name, record_id):
    """
    Removes a record from a table if it exists.
    """
    conn, cur = connect()

    query = 'DELETE FROM ' + table_name + ' WHERE id = ?'

    try:
        cur.execute(query, record_id)
    except sqlite3.Error as e:
        print(e)

    commit_close(conn)


get_queries = {
    "devices": """
    SELECT
        devices.id,
        devices.name,
        devices.description,
        JSON_GROUP_ARRAY(JSON_OBJECT('id', pets.id, 'name', pets.name)) AS pets
    FROM devices
    LEFT JOIN access ON devices.id = access.device_id
    INNER JOIN pets ON access.pet_id = pets.id
    GROUP BY devices.id;
    """,
    "pets": """
    SELECT
        pets.id AS pet_id,
        pets.name AS pet_name,
        JSON_GROUP_ARRAY(JSON_OBJECT('id', devices.id, 'name', devices.name)) AS devices
    FROM pets
    LEFT JOIN access ON pets.id = access.pet_id
    INNER JOIN devices ON access.device_id = devices.id
    GROUP BY pets.id;
    """,
    "history": """
    SELECT
        datetime,
        pets.name AS pet,
        devices.name AS device,
        event
    FROM history
    LEFT JOIN pets ON pets.id = history.pet_id
    LEFT JOIN devices ON history.device_id = devices.id;
    """,
}


def get_records_special(q):
    """

    """
    query = get_queries[q]

    conn, cur = connect()

    records = []

    try:
        cur.execute(query)
        columns = [column[0] for column in cur.description]
        rows = cur.fetchall()
        records = [dict(zip(columns, row)) for row in rows]
    except sqlite3.Error as e:
        print(e)

    commit_close(conn)

    return records if records else None


def add_device(device_dict):
    """
    Adds a new device to the database with unique name and mac address.
    """
    mac = device_dict["mac"]
    name = device_dict["name"]
    description = device_dict["description"]

    query = 'INSERT INTO devices (mac, name, description) VALUES (?, ?, ?);'

    conn, cur = connect()

    try:
        cur.execute(query, (mac, name, description))
    except sqlite3.IntegrityError as e:
        print("Error: ", e)

    commit_close(conn)


def edit_device(device_dict):
    """
    Updates a device's name and description.
    """
    device_id = device_dict["id"]
    name = device_dict["name"]
    description = device_dict["description"]

    query = 'UPDATE devices SET name = ?, description = ? WHERE id = ?;'

    conn, cur = connect()
    try:
        cur.execute(query, (name, description, device_id))
    except sqlite3.Error as e:
        print(e)

    commit_close(conn)


def add_pet(pet_dict):
    """
    Add a new pet to the database.
    """
    rfid = pet_dict["rfid"]
    name = pet_dict["name"]
    photo = pet_dict["photo"]

    query = 'INSERT INTO pets (rfid, name, photo_filename) VALUES (?, ?, ?);'

    conn, cur = connect()

    try:
        cur.execute(query, (rfid, name, photo))
    except sqlite3.IntegrityError as e:
        print("Error: ", e)

    commit_close(conn)


def edit_pet(pet_dict):
    """
    Change name or photo of a pet.
    """
    pet_id = pet_dict["id"]
    name = pet_dict["name"]
    photo = pet_dict["photo"]

    query = 'UPDATE pets SET name = ?, photo_filename = ? WHERE id = ?;'

    conn, cur = connect()
    try:
        cur.execute(query, (name, photo, pet_id))
    except sqlite3.Error as e:
        print(e)

    commit_close(conn)


def change_pet_rfid(pet_dict):
    """
    Change only RFID of a pet.
    """
    pet_id = pet_dict["id"]
    pet_rfid = pet_dict["rfid"]

    query = 'UPDATE pets SET rfid = ? WHERE id = ?;'

    conn, cur = connect()
    try:
        cur.execute(query, (pet_rfid, pet_id))
    except sqlite3.Error as e:
        print(e)

    commit_close(conn)


# todo sprawdzić czy rekordy z danym id istnieją w tabelach pets i devices
def add_access(pet_id, device_id):
    """
    Grant access to a device for a pet.
    """

    conn, cur = connect()

    query = 'SELECT COUNT(*) FROM access WHERE pet_id = ? AND device_id = ?;'

    cur.execute(query, (pet_id, device_id))
    count = cur.fetchone()[0]

    if count == 0:
        query = 'INSERT INTO access (pet_id, device_id) VALUES (?, ?);'

        try:
            cur.execute(query, (pet_id, device_id))
        except sqlite3.IntegrityError as e:
            print("Error: ", e)

    commit_close(conn)


# todo tutaj też sprawdzenie czy te rekordy istnieją w pets i devices
def add_event(pet_id, device_id, event_type):
    if event_type == 'OPEN':
        print('open')
    elif event_type == 'CLOSE':
        print('close')
    elif event_type == 'DENIED':
        print('access denied')

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = 'INSERT INTO history (datetime, pet_id, device_id, event) VALUES (?, ?, ?, ?)'

    conn, cur = connect()

    try:
        cur.execute(query, (now, pet_id, device_id, event_type))
    except sqlite3.IntegrityError as e:
        print("Error: ", e)

    commit_close(conn)
