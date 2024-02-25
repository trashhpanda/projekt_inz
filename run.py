import threading
from raspberry import rpi_run
from app import app_run

rfid_event = threading.Event()


if __name__ == '__main__':
    flask_thread = threading.Thread(target=app_run)
    rpi_thread = threading.Thread(target=rpi_run)

    flask_thread.start()
    rpi_thread.start()

    flask_thread.join()
    rpi_thread.join()
