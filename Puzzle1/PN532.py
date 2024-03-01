
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

class Rfid_PN532:

    def read_uid(self):
        
        i2c = busio.I2C(board.SCL, board.SDA)
        reset_pin = DigitalInOut(board.D6)
        req_pin = DigitalInOut(board.D12)
        pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)
        ic, ver, rev, support = pn532.firmware_version
        pn532.SAM_configuration()
        
        uid = None
        while uid is None:

            uid = pn532.read_passive_target(timeout = 0.5)
        
        return uid.hex().upper()

if __name__ == "__main__":

    rf = Rfid_PN532()
    uid = rf.read_uid()
    print(uid)
