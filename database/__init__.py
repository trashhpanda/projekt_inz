import database.db_functions as db
from database.db_functions import *
#
# dev = {
#     "mac": "666454",
#     "name": "eeee",
#     "description": "csdc"
# }
#
# dev2 = {
#     "id": "3",
#     "name": "yyyy",
#     "description": "csdc"
# }
#
# pet = {
#     "rfid": "586756",
#     "name": "kot",
#     "photo": "newton.jpeg"
# }
#
# pet2 = {
#     "id": "3",
#     "name": "Newton",
#     "photo": "newton.jpeg"
# }
#
# pet3 = {
#     "id": "1",
#     "rfid": "666"
# }
#
# if __name__ == '__main__':
    # db.create_tables()
    #   db.add_device(dev)
    #   db.edit_device(dev2)
    # db.remove_device('2')
    # devices = db.get_devices()
    # for device in devices:
    #     print(device)
    # db.add_pet(pet)
    # db.edit_pet(pet2)
    # db.remove_pet('4')
    # db.change_pet_rfid(pet3)
    # db.delete_record_by_id('pets', '3')
    # pets = db.get_records('pets')
    # for pet in pets:
    #     print(pet)
    # db.add_access(3, 7)
    # db.delete_record_by_id('access', '3')
    # acc = db.get_records('access')
    # for a in acc:
    #     print(a)
    # db.add_event(1, 2, 'OPEN')
    # history = db.get_records('history')
    # for h in history:
    #     print(h)


#
# q = "SELECT name FROM sqlite_master WHERE type='table';"
#
# conn, cur = db.connect()
# cur.execute(q)
# rows = cur.fetchall()
#
# for row in rows:
#     print(row)
#
# table_names = rows
# for table_name in table_names:
#     print(f"Table: {table_name[0]}")
#
#     # Fetch column information
#     cur.execute(f"PRAGMA table_info({table_name[0]});")
#     columns_info = cur.fetchall()
#
#     # Display column names and types
#     for column_info in columns_info:
#         print(f"  {column_info[1]} - {column_info[2]}")
#
#     print()  # Add a newline for better readability
