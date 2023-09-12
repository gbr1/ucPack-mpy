from time import sleep_ms
from machine import UART, Pin, SPI
from ucPack import ucPack

packeter = ucPack(210, 65, 35)

# ESP32-S3 settings
uart = UART(1, baudrate=115200, tx=43, rx=44)


while True:
    packeter.packetC1F(ord('E'), 0.11)
    uart.write(packeter.msg[0:packeter.msg_size])
    sleep_ms(100)

    packeter.packetC4F(ord('J'), 0.12, 1.13, 2.22, -5.0)
    uart.write(packeter.msg[0:packeter.msg_size])
    sleep_ms(100)

    packeter.packetC2F(ord('G'), 1550.01, -2360.4789)
    uart.write(packeter.msg[0:packeter.msg_size])
    sleep_ms(100)

    packeter.packetC1F(ord('S'), 0.0)
    uart.write(packeter.msg[0:packeter.msg_size])
    sleep_ms(100)

    print('sleep')
    sleep_ms(1000)
