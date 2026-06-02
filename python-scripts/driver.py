#! /usr/bin/python3
################################################################################
# University of Luxembourg
# Laboratory of Algorithmics, Cryptology and Security (LACS)
#
# Side-channel analysis lab exercise
#
# Copyright (C) 2015-2023 University of Luxembourg
################################################################################

"""
This module abstracts the target board (Arduino UNO). It can be used as a
module to be imported in other applications or as stand-alone program to
quickly test the communication between the PC and the Arduino board.
"""

from __future__ import print_function
import sys
import time
import platform
import serial

# Try to detect OS, so that we can use the correct serial port
if platform.system() == "Windows":
    # Usually COM3 (COM1 & 2 are reserved)
    portName = "COM3"
else:
    portName = "/dev/ttyACM0"
    # portName = "/dev/tty"

# Opcodes. Actually only one is defined
OP_ENCRYPT = 0x01

# Status codes
ST_READY = b">"
ST_ERROR = b"?"


# Utility functions
def intToBytes(x: int):
    """
    Convert a 128-bit unsigned integer into an array of 16 bytes (characters). The
    least-significant byte will have index 0 in the array

    Args:
            x : 16-byte integer

    Returns:
            array of 16 characters
    """
    return x.to_bytes(16, "little")


def bytesToInt(b):
    """
    Converts an array of bytes (characters) into a 128-bit unsigned integer. The
    last-significant byte has index 0

    Args:
            b : array of characters

    Returns:
            corresponding unsigned int
    """
    return int.from_bytes(b, "little")


# Board driver
class Driver(object):
    """
    Typical usage of the Driver class is illustrated below and in the __main__
    section:

            driver = Driver()
            plaintext = 0x0
            ciphertext = driver.encrypt(plaintext)
            print("-- plaintext  = 0x{0:032x}".format(plaintext))
            print("-- ciphertext = 0x{0:032x}".format(ciphertext))
            driver.close()
    """

    def __init__(self):
        """
        Creates a Driver object and initiates communication with the Arduino board.
        The driver will try to read the 10 first characters from the UART buffer
        until it finds the synchronization marker '>' (i.e., ST_READY).
        """
        self.port = serial.Serial(port=portName, baudrate=38400, timeout=1)
        time.sleep(1)
        for i in range(10):
            m = self.port.read(1)
            # print(f"Byte {i+1}: {m}")
            if m == ST_READY:
                print("-> Arduino synchronized")
                break
        else:
            print("-> Synchronization error. Aborting...")
            self.port.close()
            sys.exit(-1)

    def close(self):
        """
        Closes the communication between the PC and the arduino board. The
        communication is no more possible after close() has been executed. A new
        Driver object must be created first.
        """
        self.port.close()

    def encrypt(self, data):
        """
        Encrypts data with AES-128 configured with hidden key.

        Args:
                data: integer (up to 128 bit)

        Returns:
                integer (up to 128 bit) containing the ciphertext
        """
        req = bytes([OP_ENCRYPT]) + intToBytes(data)
        self.port.write(req)
        ciphertext_bytes = self.port.read(16)
        if len(ciphertext_bytes) != 16:
            raise ValueError("Failed to read 16 bytes for ciphertext")
        return bytesToInt(ciphertext_bytes)


if __name__ == "__main__":
    driver = Driver()
    plaintext = 0x00000000000000000000000000000000
    ciphertext = driver.encrypt(plaintext)
    print("-- plaintext  = 0x{0:032x}".format(plaintext))
    print("-- ciphertext = 0x{0:032x}".format(ciphertext))
    driver.close()
