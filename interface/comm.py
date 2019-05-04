import serial
import struct
import cmd
import time
import sys


class Comm():

    BAUD          = 115200
    CMD_SCALE     = 0
    CMD_MOTOR     = 1
    REQUEST_SCALE = struct.pack('<Bf', CMD_SCALE, 0)
    MSG_SIZE      = 5

    def __init__(self, port):
        self.arduino = serial.Serial(port, baudrate=self.BAUD)

    def motor_cmd(self, val):
        return struct.pack('<Bf', self.CMD_MOTOR, val)

    def send_stop(self):
        self.arduino.write(self.motor_cmd(0.0))

    def send_speed(self, speed):
        self.arduino.write(self.motor_cmd(speed))

    def get_scale_raw(self):
        self.arduino.write(self.REQUEST_SCALE)
        (_, resp) = struct.unpack('<Bi', self.arduino.read(self.MSG_SIZE))
        return resp


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
