#!/usr/bin/python3

# Send RC5-encoded commands using RPi.GPIO class.
# Confirmed working with:
#   Cambridge Audio azur 540A v2

import RPi.GPIO as pi
from time import sleep


#############
# CONSTANTS #
#############

RC5_PER = 889 # half-bit period (microseconds)
CA_RC5_SYS = 16

# dictionary of possible commands, mapped to the code we need to send
cmd = {
        'aux': 4,
        'cd': 5,
        'tuner': 3,
        'dvd': 1,
        'av': 2,
        'tapemon': 0,
        'vol-': 16,
        'vol+': 17,
        'volup': 16,
        'voldown': 17,
        'mute': 13,
        'standby': 12,
        'bright': 18,
        'source+': 19,
        'source-': 20,
        'sourcenext': 19,
        'sourceprev': 20,
        'clipoff': 21,
        'clipon': 22,
        'muteon': 50,
        'muteoff': 51,
        'ampon': 14,
        'ampoff': 15
        }

#############
# Functions #
#############

# build RC5 message, return as int
def build_rc5(cmd):
    RC5_START = 0b100 + (0b010 * (cmd<64))
    RC5_SYS = int(CA_RC5_SYS)
    RC5_CMD = int(cmd)

    # RC-5 message has a 3-bit start sequence, a 5-bit system ID, and a 6-bit command.
    RC5_MSG = ((RC5_START & 0b111) << 11) | ((RC5_SYS & 0b11111) << 6) | (RC5_CMD & 0b111111)
    
    return RC5_MSG

# manchester encode waveform. Period is the half-bit period in microseconds.
def wave_mnch(DATA, PIN):
    pi.setmode(pi.BOARD)
    pi.setup(PIN, pi.OUT)

    # create msg
    # syntax: pigpio.pulse(gpio_on, gpio_off, delay us)
    msg = []
    for i in bin(DATA)[2:]: # this is a terrible way to iterate over bits... but it works.
        if i=='1':
            pi.output(PIN, 0)
            sleep(RC5_PER/1000000.0)
            pi.output(PIN, 1)
            sleep(RC5_PER/1000000.0)
        else:
            pi.output(PIN, 1)
            sleep(RC5_PER/1000000.0)
            pi.output(PIN, 0)
            sleep(RC5_PER/1000000.0)

    pi.output(PIN, 0)
    pi.cleanup()
    return 0

# check for positive integer
def posint(n):
    try:
        if int(n)>0:
            return int(n)
        else:
            raise ValueError
    except ValueError:
            msg = str(n) + " is not a positive integer"
            raise argparse.ArgumentTypeError(msg)

def execute(pin, command, repeat):

    # generate RC5 message (int)
    rc5_msg = build_rc5(cmd[command])

    # generate digital manchester-encoded waveform
    for i in range(repeat):
        wave_mnch(rc5_msg, pin)
