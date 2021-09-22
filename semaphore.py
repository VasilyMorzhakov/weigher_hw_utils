import logging
import socket

import serial


class Semaphore:
    def __init__(self, address, tcp=True):
        self.tcp = tcp
        if tcp:
            self.IP_address = address
        else:
            self.com_port = address

        self.status = ["red", "red", "red", "red"]
        for i in range(4):
            self.set_red(i)

    def get_status(self):
        return self.status

    def set_green(self, index):
        self.status[index] = "green"
        try:

            if self.tcp:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.IP_address, 4001))
                s.settimeout(5.0)
            else:
                s = serial.Serial(self.com_port, timeout=1)

            if index == 0:
                buf = bytearray.fromhex("01 05 00 00 FF 00 8C 3A")

            if index == 1:
                buf = bytearray.fromhex("01 05 00 01 FF 00 DD FA")

            if index == 2:
                buf = bytearray.fromhex("01 05 00 02 FF 00 2D FA")

            if index == 3:
                buf = bytearray.fromhex("01 05 00 03 FF 00 7C 3A")

            if self.tcp:
                s.send(buf)
                s.settimeout(0.2)

                try:
                    s.recv(1024)
                except Exception as e:
                    logging.error(e)
            else:
                s.write(buf)
                try:
                    s.read(len(buf))
                except Exception as e:
                    logging.error(e)

            s.close()
        except Exception as e:
            logging.error("could not set green " + str(e))

    def set_red(self, index):

        self.status[index] = "red"
        try:
            if self.tcp:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.IP_address, 4001))
                s.settimeout(0.2)
            else:
                s = serial.Serial(self.com_port, timeout=1)

            if index == 0:
                buf = bytearray.fromhex("01 05 00 00 00 00 CD CA")

            if index == 1:
                buf = bytearray.fromhex("01 05 00 01 00 00 9C 0A")

            if index == 2:
                buf = bytearray.fromhex("01 05 00 02 00 00 6C 0A")

            if index == 3:
                buf = bytearray.fromhex("01 05 00 03 00 00 3D CA")


            if self.tcp:
                s.send(buf)
                s.settimeout(0.2)

                try:
                    s.recv(1024)
                except Exception as e:
                    logging.error(e)
            else:
                s.write(buf)
                try:
                    s.read(len(buf))
                except Exception as e:
                    logging.error(e)

            s.close()
        except Exception as e:
            logging.error("could not set green " + str(e))
