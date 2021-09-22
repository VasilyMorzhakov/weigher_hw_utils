import datetime
import logging
import socket
import struct


class Parsec:
    def __init__(self, server_ip, remote_ip):
        self.server_ip = server_ip
        self.remote_ip = remote_ip
        self.index = 1

    def next_index(self):
        if self.index == 255:
            self.index = 0
        else:
            self.index = self.index + 1

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.server_ip, 8873))
        self.closed=False

    def close(self):
        self.sock.close()
        self.closed=True

    def send_raw(self, data):
        if self.closed:
            self.connect()
        CRCTBL = [
            0,
            94,
            188,
            226,
            97,
            63,
            221,
            131,
            194,
            156,
            126,
            32,
            163,
            253,
            31,
            65,
            157,
            195,
            33,
            127,
            252,
            162,
            64,
            30,
            95,
            1,
            227,
            189,
            62,
            96,
            130,
            220,
            35,
            125,
            159,
            193,
            66,
            28,
            254,
            160,
            225,
            191,
            93,
            3,
            128,
            222,
            60,
            98,
            190,
            224,
            2,
            92,
            223,
            129,
            99,
            61,
            124,
            34,
            192,
            158,
            29,
            67,
            161,
            255,
            70,
            24,
            250,
            164,
            39,
            121,
            155,
            197,
            132,
            218,
            56,
            102,
            229,
            187,
            89,
            7,
            219,
            133,
            103,
            57,
            186,
            228,
            6,
            88,
            25,
            71,
            165,
            251,
            120,
            38,
            196,
            154,
            101,
            59,
            217,
            135,
            4,
            90,
            184,
            230,
            167,
            249,
            27,
            69,
            198,
            152,
            122,
            36,
            248,
            166,
            68,
            26,
            153,
            199,
            37,
            123,
            58,
            100,
            134,
            216,
            91,
            5,
            231,
            185,
            140,
            210,
            48,
            110,
            237,
            179,
            81,
            15,
            78,
            16,
            242,
            172,
            47,
            113,
            147,
            205,
            17,
            79,
            173,
            243,
            112,
            46,
            204,
            146,
            211,
            141,
            111,
            49,
            178,
            236,
            14,
            80,
            175,
            241,
            19,
            77,
            206,
            144,
            114,
            44,
            109,
            51,
            209,
            143,
            12,
            82,
            176,
            238,
            50,
            108,
            142,
            208,
            83,
            13,
            239,
            177,
            240,
            174,
            76,
            18,
            145,
            207,
            45,
            115,
            202,
            148,
            118,
            40,
            171,
            245,
            23,
            73,
            8,
            86,
            180,
            234,
            105,
            55,
            213,
            139,
            87,
            9,
            235,
            181,
            54,
            104,
            138,
            212,
            149,
            203,
            41,
            119,
            244,
            170,
            72,
            22,
            233,
            183,
            85,
            11,
            136,
            214,
            52,
            106,
            43,
            117,
            151,
            201,
            74,
            20,
            246,
            168,
            116,
            42,
            200,
            150,
            21,
            75,
            169,
            247,
            182,
            232,
            10,
            84,
            215,
            137,
            107,
            53,
        ]
        CRC = 0x5A
        for i in range(len(data)):
            CRC = CRCTBL[CRC ^ data[i]]

        data.append(CRC)
        ar = bytearray(data)
        self.sock.settimeout(1.0)
        self.sock.sendto(ar, (self.remote_ip, 8872))

        try:
            data, addr = self.sock.recvfrom(1024)
        except socket.timeout:
            logging.error("Write timeout on socket")
            self.close()
            return None

        return data

    def get_version(self):
        data = [self.index, 0x01, 0x83, 0xC0, 0x01, 0x00, 0x00, 0x6A, 0x00, 0x00]
        self.next_index()
        return self.send_raw(data)

    def set_RTC(self):
        seconds = datetime.datetime.now().second
        minute = datetime.datetime.now().minute
        hour = datetime.datetime.now().hour

        day_week = 0
        day = datetime.datetime.now().day
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        year_low_byte = year - int(year / 256) * 256
        year_high_byte = int(year / 256)

        data = [
            self.index,
            0x01,
            0x82,
            0xC0,
            0x01,
            0x00,
            0x00,
            0xC2,
            0x00,
            0x08,
            seconds,
            minute,
            hour,
            day_week,
            day,
            month,
            year_low_byte,
            year_high_byte,
        ]
        self.next_index()
        return self.send_raw(data)

    def clear_transaction(self):
        data = [self.index, 0x00, 0x82, 0xC0, 0x01, 0x00, 0x00, 0xA2, 0x00, 0x00]
        self.next_index()
        return self.send_raw(data)

    def ask_transaction(self):
        data = [self.index, 0x00, 0x84, 0xC0, 0x01, 0x00, 0x00, 0x41, 0x00, 0x00]
        self.next_index()
        res = self.send_raw(data)

        if res is None:
            return None

        L = res[9]
        if L == 0:
            return None

        res = res[10: 10 + L]
        print(res.hex())
        return struct.unpack("I", res[15:19])[0], int(res[9])
