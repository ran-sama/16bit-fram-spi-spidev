#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import spidev, sys

op_mode = sys.argv[1]
spi = spidev.SpiDev()
spi.open(0,0)
sys.stdin.reconfigure(encoding='latin-1')
sys.stdout.reconfigure(encoding='latin-1')

#20MHz
spi.max_speed_hz = 20*1000*1000
spi.mode = 0b00

READ = 3
WRITE = 2
WRITE_EN = 6
WRITE_DIS = 4

BUF_SIZE = 32
chip_size = 32768

def writeByteAll(addr,chunk):
    msb = addr >> 8
    lsb = addr & 0xFF
    spi.xfer2([WRITE_EN])
    spi.xfer2([WRITE,msb,lsb]+chunk)

def readByteAll():
    for i in range(int(chip_size/BUF_SIZE)):
        memory_address = i*BUF_SIZE
        msb = memory_address >> 8
        lsb = memory_address & 0xFF
        val = spi.xfer2([READ,msb,lsb,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00])
        blob = list(val[3:])
        for ch in map(chr,blob):
            sys.stdout.write(ch)
            sys.stdout.flush()

if (op_mode == "w"):
    data = sys.stdin.read()
    i=0
    j=0
    chunk = []
    while i * BUF_SIZE < chip_size:
        chunk = [ord(data[j+i*BUF_SIZE]) for j in range(BUF_SIZE)]
        writeByteAll(i*BUF_SIZE, chunk)
        i += 1
    spi.xfer2([WRITE_DIS])
elif (op_mode == "r"):
    readByteAll()

spi.close()
