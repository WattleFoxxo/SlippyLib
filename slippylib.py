import serial
import threading
import time

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
    def on_ready(self, addr): pass

    def __receive(self):
        while True:
            line = self.device.readline().decode().strip()
            if line:
                #print(line)
                split_msg = line.split(" ")

                if split_msg[0] == "MESSAGE":
                    dest_address = split_msg[1]
                    src_address = split_msg[2]
                    msg_id = split_msg[3]
                    msg_len = split_msg[4]
                    message = split_msg[5].split(",")
                    rssi = split_msg[6]
                    snr = split_msg[7]

                    self.on_message(dest_address, src_address, rssi, snr, msg_id, "".join(str(chr(int(char))) for char in message))

                if split_msg[0] == "READY":
                    self.on_ready = split_msg[1]
                

    def send(self, address, message):
        if (len(message) > 128):
            return "message too big"
        self.device.write(f"0 {' '.join(str(id) for id in address.split('.'))} {len(message)} {' '.join(str(ord(char)) for char in message)} 0\n".encode("ascii"))