import serial
import threading
import time

## Defs
MESSAGE_TAG = "[MESSAGE]"
ADDRESS_TAG = "[ADDRESS]"
ERROR_TAG   = "[ERROR]"
INFO_TAG    = "[INFO]"

class SlipPy:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.address = "0.0.0.0"

        self.device = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)

        self.device.close()
        self.device.open()

        self.receive_thread = threading.Thread(target=self.__receive)
        self.receive_thread.start()


    def on_message(self, dest_address, src_address, rssi, snr, msg_id, message): pass # print raw message
    def on_error(self, error): pass
    def on_info(self, info): pass

    def __receive(self):
        while True:
            line = self.device.readline().decode().strip()
            if line:
                split_msg = line.split(";")

                if split_msg[0] == MESSAGE_TAG:
                    dest_address = split_msg[1]
                    src_address = split_msg[2]
                    rssi = split_msg[3]
                    snr = split_msg[4]
                    msg_id = split_msg[5]
                    msg_len = split_msg[6]

                    self.on_message(dest_address, src_address, rssi, snr, msg_id, "".join(str(part) for part in split_msg[7:]))

                if split_msg[0] == ADDRESS_TAG:
                    self.address = split_msg[1]
                
                if split_msg[0] == ERROR_TAG:
                    self.on_error(split_msg[1])
                
                if split_msg[0] == INFO_TAG:
                    self.on_info(split_msg[1])

    def send(self, address, message):
        self.device.write(f"{address};{message}\0".encode("ascii"))