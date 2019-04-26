#! /usr/bin/env python3
import cmd
import sys
import serial
import struct

class ProtoController(cmd.Cmd):
    intro = 'Prototype 1 stepper controller'

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.s = serial.Serial('/dev/ttyACM0')

    def do_speed(self, val):
        if val == '':
            return
        self.s.write(struct.pack("<Bi", 0, int(val)))

    def do_time(self, sec):
        if sec == '':
            return
        self.s.write(struct.pack("<Bf", 1, float(sec)))

    def do_micro(self, micro):
        if micro == "":
            return
        self.s.write(struct.pack("<Bi", 2, int(micro)))

    def do_deg(self, deg):
        if deg == '':
            return
        self.s.write(struct.pack("<Bi", 3, int(deg)))

    def do_stop(self, params=None):
        self.s.write(struct.pack("<Bf", 1, 0.0))

    def do_exit(self, *args):
        sys.exit()

    def do_quit(self, *args):
        sys.exit()


if __name__ == "__main__":
    ProtoController().cmdloop()
