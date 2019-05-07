import serial
import struct
import cmd
import time
import sys
from collections import deque


class Comm():

    BAUD          = 115200
    CMD_SCALE     = 0
    CMD_MOTOR     = 1
    REQUEST_SCALE = struct.pack('<Bf', CMD_SCALE, 0)
    MSG_SIZE      = 5
    TIMEOUT       = 0.5
    MAX_RETRIES   = 3
    M             = -4.90471
    B             = 3426.251
    FILTER_LEN    = 20
    ROUND_TO      = 5

    def __init__(self, port):
        self.arduino = serial.Serial(port, baudrate=self.BAUD,
                                     timeout=self.TIMEOUT)
        self.filter = deque(maxlen=Comm.FILTER_LEN)

    def motor_cmd(self, val):
        return struct.pack('<Bf', self.CMD_MOTOR, val)

    def send_msg(self, msg):

        self.arduino.write(msg)
        read = self.arduino.read(self.MSG_SIZE)
        tries = 1

        while len(read) != self.MSG_SIZE and tries < self.MAX_RETRIES:
            self.arduino.write(msg)
            read = self.arduino.read(self.MSG_SIZE)
            tries += 1
        if len(read) == self.MSG_SIZE:
            return read
        else:
            raise Exception('Error communicating with the Arduino')

    def send_stop(self):
        self.send_speed(0.0)

    def send_speed(self, speed):
        # read the response and ignore it
        self.send_msg(self.motor_cmd(speed))

    def get_scale_raw(self):
        msg = self.send_msg(self.REQUEST_SCALE)
        (_, resp) = struct.unpack('<Bi', msg)
        return resp

    def get_weight(self):
        self.filter.append(self.get_scale_raw())
        return Comm.ROUND_TO * round((Comm.M * sum(self.filter)
                                      / Comm.FILTER_LEN + Comm.B)
                                     / Comm.ROUND_TO)


class CommTest(cmd.Cmd):
    intro = '472 Arduino test program'

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.comm = Comm('/dev/ttyACM0')

    def do_scale(self, time_s):
        if time == '':
            return
        t_end = time.time() + float(time_s)
        while time.time() < t_end:
            print(self.comm.get_scale_raw())
            time.sleep(0.1)

    def do_motor(self, speed):
        if speed == '':
            return
        self.comm.send_speed(float(speed))

    def do_stop(self, params=None):
        self.comm.send_stop()

    def do_exit(self, params=None):
        sys.exit()

    def do_quit(self, params=None):
        sys.exit()


if __name__ == '__main__':
    CommTest().cmdloop()
