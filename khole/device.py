from bluetooth.ble import DiscoveryService
from gattlib import GATTRequester


class kHoleDevice(object):

    def __init__(self):
        self.device = None

    def connect_via_scan(self):
        service = DiscoveryService()
        devices = service.discover(2)
        for address, name in devices.items():
            if name == "kGoal":
                self.device = GATTRequester(address)
                return True
        return False

    def get_reading(self):
        msg = self.device.read_by_handle(0x2a)[0]
        calibrated = ord(msg[3]) << 8 | ord(msg[4])
        uncalibrated = ord(msg[5]) << 8 | ord(msg[6])
        return (calibrated, uncalibrated)

    def set_motor_cmd(self, motor_idx, on):
        self.device.write_by_handle(0x41,
                                    str(bytearray([0x00, motor_idx, 0x07, 0x00, 0x1b if on else 0x00, 0x00, 0x00, 0x96, 0x00, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])))

    def set_squeeze_pillow(self, on):
        self.set_motor_cmd(1, on)

    def set_control_arm(self, on):
        self.set_motor_cmd(2, on)

