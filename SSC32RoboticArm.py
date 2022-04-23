import serial.serialutil
import serial
import ssc32
import time


class SSC32RoboticArm:
    def __init__(self, port, baud):
        self.default_dur = 800
        self.extended_dur = 100
        self.serial_port = port
        self.baud_rate = baud
        self.connected = False
        self.posmax = 2500
        self.posmin = 500

        # try:
        #     self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        #     print(f"Connected to {self.serial_port, self.ser}")
        #     self.connected = True
        # except serial.serialutil.SerialException:
        #     self.connected = False
        #     print(f"Serial port {self.serial_port} not found")
        #     pass
        try:
            self.ssc = ssc32.SSC32(self.serial_port, self.baud_rate)
            self.connected = True
            self.default_pos()
        except serial.serialutil.SerialException:
            print(f"Port {self.serial_port} not found.")
            self.connected = False
            pass

    def default_pos(self):
        if self.connected:
            pos = self.__map_to_deg(90)
            print(pos)
            self.pos_0 = pos
            self.pos_1 = pos
            self.pos_2 = pos
            self.pos_3 = pos
            self.pos_4 = 1000


            self.move_ssc(0, self.pos_0, self.extended_dur)
            self.move_ssc(1, self.pos_1, self.extended_dur)
            self.move_ssc(2, self.pos_2, self.extended_dur)
            self.move_ssc(3, self.pos_3, self.extended_dur)
            self.move_ssc(14, self.pos_4, self.extended_dur)

    def move_ssc(self, servo, pos, dur):
        if self.connected:
            # self.ser.write(bytes(f"#{servo} P{pos} T{dur} <cr>", "utf-8"))
            self.ssc.commit(time=dur)
            self.ssc[servo].position = pos

    def __map_to_deg(self, degree):
        if 0 <= degree <= 180:
            pos = degree / 180 * (self.posmax - self.posmin) + self.posmin
            return pos
        else:
            print("Degree out of range")

    # def
