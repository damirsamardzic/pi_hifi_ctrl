#!/usr/bin/python3

import sys
import argparse
import libamp_rpigpio as libamp


# Build argument parser
parser = argparse.ArgumentParser(description="Control Cambridge Audio amplifiers using RPi.GPIO class.")
parser.add_argument('--pin', nargs='?', default=7, type=int)
parser.add_argument('--repeat', nargs='?', default=1, type=libamp.posint)
parser.add_argument('command', nargs=1, choices=libamp.cmd.keys())
args = parser.parse_args()

command = args.command[0].lower()
print("Sending '" + command + "' command to pin " + str(args.pin))

if args.repeat != 1:
    print(str(args.repeat) + " times")

libamp.execute(args.pin, command, args.repeat)

sys.exit(0)
