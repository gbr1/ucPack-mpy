import struct

from CircularBuffer import CircularBuffer


class ucPack:

    def __init__(self, buffer_size: int, start_index: int = ord('A'), end_index: int = ord('#')):
        self.buffer_size = buffer_size
        self.buffer = CircularBuffer(buffer_size)
        self.start_index = start_index
        self.end_index = end_index

        self.payload = bytearray(0)

        self.msg = bytearray(buffer_size)
        self.msg_size = 0

    def checkPayload(self) -> bool:

        self.payload = bytearray(0)

        # check if buffer is empty
        if self.buffer.isEmpty():
            return False

        # check the index byte
        while not (self.buffer.top() == self.start_index) and (self.buffer.getSize() > 0):
            self.buffer.pop()

        # exit if only message index is received
        if self.buffer.getSize() <= 1:
            return False

        # get the payload dimension
        payload_size = self.buffer[1]

        # check if packet is complete
        if self.buffer.getSize() < (payload_size + 4):     # memo: index|length|msg|stop|crc8
            return False

        # check if stop byte is correct
        if self.buffer[payload_size + 2] != self.end_index:
            return False

        # crc checking
        for i in range(0, payload_size):
            self.payload.append(self.buffer[i + 2])

        if self.crc8(self.payload[0:payload_size]) != self.buffer[payload_size + 3]:
            self.buffer.pop()   # delete the index so it is possible to recheck
            return False

        # clear the buffer
        for _ in range(0, payload_size + 4):
            self.buffer.pop()

        return True

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

    def payloadTop(self):
        return self.payload[0]

    def packetC1F(self, code: int, f: float) -> int:
        self.msg[0] = self.start_index & 0xFF
        self.msg[1] = 5
        self.msg[2] = code & 0xFF
        self.msg[3:7] = bytearray(struct.pack("f", f))
        self.msg[7] = self.crc8(self.msg[2:7])
        self.msg[8] = self.end_index & 0xFF
        self.msg_size = 9
        return self.msg_size

    def unpacketC1F(self) -> (int, float):
        code = self.payload[0]
        f = struct.unpack("f", self.payload[1:5])[0]
        return code, f

    def packetC2F(self, code: int, f1: float, f2: float) -> int:
        self.msg[0] = self.start_index & 0xFF
        self.msg[1] = 5
        self.msg[2] = code & 0xFF
        self.msg[3:7] = bytearray(struct.pack("f", f1))
        self.msg[7:11] = bytearray(struct.pack("f", f2))
        self.msg[11] = self.crc8(self.msg[2:7])
        self.msg[12] = self.end_index & 0xFF
        self.msg_size = 13
        return self.msg_size

    def unpacketC2F(self) -> (int, float, float):
        code = self.payload[0]
        f1 = struct.unpack("f", self.payload[1:5])[0]
        f2 = struct.unpack("f", self.payload[5:9])[0]
        return code, f1, f2

    def packetC4F(self, code: int, f1: float, f2: float, f3: float, f4: float) -> int:
        self.msg[0] = self.start_index & 0xFF
        self.msg[1] = 5
        self.msg[2] = code & 0xFF
        self.msg[3:7] = bytearray(struct.pack("f", f1))
        self.msg[7:11] = bytearray(struct.pack("f", f2))
        self.msg[11:15] = bytearray(struct.pack("f", f3))
        self.msg[15:19] = bytearray(struct.pack("f", f4))
        self.msg[19] = self.crc8(self.msg[2:7])
        self.msg[20] = self.end_index & 0xFF
        self.msg_size = 21
        return self.msg_size

    def unpacketC4F(self) -> (int, float, float, float, float):
        code = self.payload[0]
        f1 = struct.unpack("f", self.payload[1:5])[0]
        f2 = struct.unpack("f", self.payload[5:9])[0]
        f3 = struct.unpack("f", self.payload[9:13])[0]
        f4 = struct.unpack("f", self.payload[13:17])[0]
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
        self.msg[35] = self.crc8(self.msg[2:7])
        self.msg[36] = self.end_index & 0xFF
        self.msg_size = 37
        return self.msg_size

    def unpacketC8F(self) -> (int, float, float, float, float, float, float, float, float):
        code = self.payload[0]
        f1 = struct.unpack("f", self.payload[1:5])[0]
        f2 = struct.unpack("f", self.payload[5:9])[0]
        f3 = struct.unpack("f", self.payload[9:13])[0]
        f4 = struct.unpack("f", self.payload[13:17])[0]
        f5 = struct.unpack("f", self.payload[17:21])[0]
        f6 = struct.unpack("f", self.payload[21:25])[0]
        f7 = struct.unpack("f", self.payload[25:29])[0]
        f8 = struct.unpack("f", self.payload[29:33])[0]
        return code, f1, f2, f3, f4, f5, f6, f7, f8


if __name__ == "__main__":
    data = bytearray([0x0b, 0xAA, 0x01, 0xFF, 0x1e])
    c = ucPack.crc8(data)
    print(hex(c))

    packeter = ucPack(buffer_size=10, start_index=ord('S'), end_index=ord('E'))
    packeter.buffer.push(ord('S'))
    packeter.buffer.push(5)
    packeter.buffer.push(0x0b)
    packeter.buffer.push(0xAA)
    packeter.buffer.push(0x01)
    packeter.buffer.push(0xFF)
    packeter.buffer.push(0x1e)
    packeter.buffer.push(ord('E'))
    packeter.buffer.push(c)

    packeter.checkPayload()

    print(packeter.payload)

    print(packeter.unpacketC1F())

    code_, num_ = packeter.unpacketC1F()

    packeter.packetC1F(code_, num_)

    print(packeter.msg)
