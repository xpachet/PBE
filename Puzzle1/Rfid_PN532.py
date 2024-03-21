
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

class Rfid_PN532:
    

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.reset_pin = DigitalInOut(board.D6)
        self.req_pin = DigitalInOut(board.D12)
        self.pn532 = PN532_I2C(self.i2c, reset=self.reset_pin, req=self.req_pin)
        self.pn532.SAM_configuration()
        
    def read_uid(self):

        self.uid = None
        while self.uid is None:

            self.uid = self.pn532.read_passive_target(timeout = 0.5)
        
        return self.uid.hex().upper()

if __name__ == "__main__":

    rf = Rfid_PN532()
    uid = rf.read_uid()
    print(uid)
