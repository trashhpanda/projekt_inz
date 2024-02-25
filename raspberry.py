import RPi.GPIO as GPIO
from gpiozero import Servo, MotionSensor
from mfrc522 import SimpleMFRC522
from time import sleep
import threading
from database.db_functions import get_access, get_pet_id, add_event

GPIO.setmode(GPIO.BCM)

scan_event = threading.Event()
lid_opened_event = threading.Event()

reader = SimpleMFRC522()

servo = Servo(12, initial_value=None)

pir = MotionSensor(18)


def scan():
    rfid = None
    try:
        rfid = reader.read_id()
        print('scanned rfid: ' + str(rfid))
    except Exception as e:
        print(e)
    return str(rfid)


def open_lid():
    servo.value = -1
    sleep(3)
    servo.value = None
    lid_opened_event.set()
    print('opened lid')


def close_lid():
    servo.value = 1
    sleep(3)
    servo.value = None
    lid_opened_event.clear()
    print('closed lid')


def rpi_run():
    try:
        n = 0
        while True:
            n += 1
            print(n)
            if not scan_event.is_set():
                rfid = reader.read_id()
                pet = get_pet_id(rfid)
                if rfid:
                    access = get_access('1')
                    if str(rfid) in access:
                        print(pet)
                        print("access granted. opening lid.")
                        open_lid()
                        add_event(pet, '1', 'OPEN')
                        sleep(5)
                        pir.wait_for_no_motion()
                        print("no motion detected. closing lid.")
                        close_lid()
                        add_event(pet, '1', 'CLOSE')
                    else:
                        print("access denied")
                        add_event(pet, '1', 'DENIED') if pet else add_event('0', '1', 'DENIED')
                        sleep(5)
                        pir.wait_for_no_motion()
    finally:
        print("end")
        GPIO.cleanup()
