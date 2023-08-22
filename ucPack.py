import struct


class ucPack:

    def __init__(self, buffer_size: int, start_index: int = ord('A'), end_index: int = ord('#')):
        self.buffer_size = buffer_size
        self.start_index = start_index
        self.end_index = end_index

        self.payload = bytearray(buffer_size)
        self.payload_size = 0

        self.msg = bytearray(buffer_size)
        self.msg_size = 0

    @staticmethod
    def crc8(data):
        crc = 0x00

        for extract in data:
            for _ in range(0, 8):
                sum = (crc ^ extract) & 0x01
                crc = crc >> 1
                if sum:
                    crc = crc ^ 0x8C
                extract = extract >> 1

        return crc

    def packetC1F(self, code: int, f: float) -> int:
        self.msg[0] = self.start_index & 0xFF
        self.msg[1] = 5
        self.msg[2] = code & 0xFF
        self.msg[3:7] = bytearray(struct.pack("f", f))
        self.msg[7] = self.end_index & 0xFF
        self.msg[8] = self.crc8(self.msg[2:7])
        self.msg_size = 9
        return self.msg_size

    def unpacketC1F(self) -> (int, float):
        code = self.payload[0]
        f = struct.unpack("f", self.payload[1:5])
        return code, f

    def packetC2F(self, code: int, f1: float, f2: float) -> int:
        self.msg[0] = self.start_index & 0xFF
        self.msg[1] = 5
        self.msg[2] = code & 0xFF
        self.msg[3:7] = bytearray(struct.pack("f", f1))
        self.msg[7:11] = bytearray(struct.pack("f", f2))
        self.msg[11] = self.end_index & 0xFF
        self.msg[12] = self.crc8(self.msg[2:7])
        self.msg_size = 13
        return self.msg_size

    def unpacketC2F(self) -> (int, float, float):
        code = self.payload[0]
        f1 = struct.unpack("f", self.payload[1:5])
        f2 = struct.unpack("f", self.payload[5:9])
        return code, f1, f2

    def packetC4F(self, code: int, f1: float, f2: float, f3: float, f4: float) -> int:
        self.msg[0] = self.start_index & 0xFF
        self.msg[1] = 5
        self.msg[2] = code & 0xFF
        self.msg[3:7] = bytearray(struct.pack("f", f1))
        self.msg[7:11] = bytearray(struct.pack("f", f2))
        self.msg[11:15] = bytearray(struct.pack("f", f3))
        self.msg[15:19] = bytearray(struct.pack("f", f4))
        self.msg[19] = self.end_index & 0xFF
        self.msg[20] = self.crc8(self.msg[2:7])
        self.msg_size = 21
        return self.msg_size

    def unpacketC4F(self) -> (int, float, float, float, float):
        code = self.payload[0]
        f1 = struct.unpack("f", self.payload[1:5])
        f2 = struct.unpack("f", self.payload[5:9])
        f3 = struct.unpack("f", self.payload[9:13])
        f4 = struct.unpack("f", self.payload[13:17])
        return code, f1, f2, f3, f4

    def packetC8F(self, code: int, f1: float, f2: float, f3: float, f4: float,
                  f5: float, f6: float, f7: float, f8: float) -> int:
        self.msg[0] = self.start_index & 0xFF
        self.msg[1] = 5
        self.msg[2] = code & 0xFF
        self.msg[3:7] = bytearray(struct.pack("f", f1))
        self.msg[7:11] = bytearray(struct.pack("f", f2))
        self.msg[11:15] = bytearray(struct.pack("f", f3))
        self.msg[15:19] = bytearray(struct.pack("f", f4))
        self.msg[19:23] = bytearray(struct.pack("f", f5))
        self.msg[23:27] = bytearray(struct.pack("f", f6))
        self.msg[27:31] = bytearray(struct.pack("f", f7))
        self.msg[31:35] = bytearray(struct.pack("f", f8))
        self.msg[35] = self.end_index & 0xFF
        self.msg[36] = self.crc8(self.msg[2:7])
        self.msg_size = 37
        return self.msg_size

    def unpacketC8F(self) -> (int, float, float, float, float, float, float, float, float):
        code = self.payload[0]
        f1 = struct.unpack("f", self.payload[1:5])
        f2 = struct.unpack("f", self.payload[5:9])
        f3 = struct.unpack("f", self.payload[9:13])
        f4 = struct.unpack("f", self.payload[13:17])
        f5 = struct.unpack("f", self.payload[17:21])
        f6 = struct.unpack("f", self.payload[21:25])
        f7 = struct.unpack("f", self.payload[25:29])
        f8 = struct.unpack("f", self.payload[29:33])
        return code, f1, f2, f3, f4, f5, f6, f7, f8


if __name__ == "__main__":
    data = bytearray([0x0b, 0xAA, 0x01, 0xFF])
    c = ucPack.crc8(data)
    print(hex(c))
