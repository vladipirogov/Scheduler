import serial
import threading
from concurrent.futures import ThreadPoolExecutor
from app import socketio


class SerialService:
    def __init__(self):
        self.connected = False
        self.serPort = '/dev/ttyS0'
        self.baudRate = 9600
        self.ser = serial.Serial(self.serPort, self.baudRate, timeout=1)
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None

    def send_to_arduino(self, send_str):
        if not self.ser.is_open:
            self.ser.open()
        self.connected = True
        threading.Timer(2.0, self.stop_reading).start()
        self.ser.write(bytes(send_str, 'UTF-8'))
        self.future = self.executor.submit(self.read_from_port())

    def handle_data(self, data):
        socketio.emit('message', data, callback=self.message_received)

    def stop_reading(self):
        self.connected = False
        print("stop")

    def read_from_port(self):
        while self.connected:
            reading = self.ser.readline().decode()
            self.handle_data(reading)

    def message_received(self):
        print('message was received!!!')
