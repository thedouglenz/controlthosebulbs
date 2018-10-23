""" An object oriented approach to flux LED and Magiclight bulb programming with
random sample methods for seasonal illumination and/or pulsatings.

thedouglenz@gmail.com
Oct, 2018
"""
import socket, time
import os


# Bulb configuration; These are mine. Set your own with
# env vars: MAGIC_BULB_IP and MAGIC_BULB_PORT
# 5577 is the default port for Magic Home lighting products
IP_ADDRESS = '10.10.123.3'
PORT = 5577

# Use env var MAGIC_LIGHT_DEBUG to set; determines to what extent to
# print debug info to stdout
DEBUG_LEVEL = 0

# List of colors I'll probably use
ORANGE      = (255, 128, 0)
PURPLE      = (255, 0, 255)
RED         = (255, 0, 0)
BLUE        = (0, 0, 255)
GREEN       = (0, 255, 0)
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
DARK_PURPLE = (76, 0, 153)
BLOOD_RED   = (202, 0, 0)
XMAS_RED    = (253, 89, 89)
XMAS_GREEN  = (57, 252, 96)
PINK        = (255, 153, 255)


class Bulb:
    """A Magiclight bulb or a smart light bulb using flux LED protocol"""

    def __init__(self, ip_address, port):
        """Constructor; takes IP address and port number and initializes its
        own socket"""

        self.ip_address = ip_address
        self.port = port
        self.s = socket.socket()

    def connect(self):
        """Try to open a socket with this bulb's port"""
        try:
            self.s.connect((self.ip_address, self.port))
        except:
            print "Error connecting to bulb"

    def _send(self, message):
        """Send a message to the bulb"""
        try:
            self.s.send("81:8a:8b:96".replace(':', '').decode('hex'))
            self.s.recv(1000)
            self.s.send("10:14:0f:08:0d:05:16:15:04:00:0f:8b"\
                    .replace(':', '').decode('hex'))
            self.s.recv(1000)
            self.s.send(message)
        except:
            print "Error sending color information to bulb"

    def update_color(self, color):
        """Given a color tuple (red, green, blue), update this bulb's color"""
        assert len(color) == 3

        # Break tuple into r, g, b
        r = color[0]
        g = color[1]
        b = color[2]

        msg = "31".replace(':', '').decode('hex')
        msg += chr(r) + chr(g) + chr(b)
        msg += "00:f0:0f".replace(':', '').decode('hex')
        msg += chr(sum(bytearray(msg)) % 256)
        #print sum(bytearray(msg[:-1])) % 256
        #print msg.encode('hex')

        self._send(msg)


def purple_green_cycle(bulb, delay):
    """Given a bulb, cycle it between purple and green with the given delay"""

    # Time between color changes must be a positive float
    # Under half a second, it starts to lag
    assert delay >= 0.5

    while 1:
        bulb.update_color(GREEN)
        time.sleep(delay)
        bulb.update_color(PURPLE)
        time.sleep(delay)


def xmas_red_green_pulse(bulb, delay):
    """Given a bulb, cycle the bulb between xmas red and green"""

    # Time between color changes must be a positive float
    # Under half a second, it starts to lag
    assert delay >= 0.5

    while 1:
        bulb.update_color(XMAS_RED)
        time.sleep(delay)
        bulb.update_color(XMAS_GREEN)
        time.sleep(delay)


def fall_orange(bulb):
    """Given a bulb, illuminate it an orange color"""
    bulb.update_color(ORANGE)


def blood_red(bulb):
    """Given a bulb, illuminate it a blood red color"""
    bulb.update_color(BLOOD_RED)


def get_bulb():
    """Create a new Bulb and open its socket"""

    if DEBUG_LEVEL >= 1:
        print "Creating a bulb at {}:{}".format(IP_ADDRESS, PORT)

    bulb = Bulb(IP_ADDRESS, PORT)
    bulb.connect()

    return bulb


def pulse(bulb, colors, delay):
    """Given a bulb, list/tuple of colors, and a delay in seconds cycle between each color
    with @delay seconds in between transitions"""

    # No reason to pulse if we just want 1 color
    assert len(colors) > 1

    # Time between color changes must be a positive float
    assert delay > 0

    if DEBUG_LEVEL >= 1:
        print "Pulsing bulb {}:{} with {} at {}s delay".format(
                IP_ADDRESS, PORT, colors, delay)

    while 1:
        for c in colors:
            bulb.update_color(c)
            time.sleep(delay)


def main():
    """Create a bulb and start some smart bulb things"""

    # Bulb creation
    bulb = get_bulb()

    # Do things with bulb
    pulse(bulb, (ORANGE, RED), 0.5)


if __name__ == "__main__":

    if 'MAGIC_BULB_IP' in os.environ:
        IP_ADDRESS = os.environ['MAGIC_BULB_IP']

    if 'MAGIC_BULB_PORT' in os.environ:
        PORT = os.environ['MAGIC_BULB_PORT']

    if "MAGIC_LIGHT_DEBUG" in os.environ:
        DEBUG_LEVEL = os.environ["MAGIC_LIGHT_DEBUG"]

    main()
