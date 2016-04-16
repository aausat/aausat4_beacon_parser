import bluebox
import fec
import binascii

class Parser(object):

    DEFAULT_FREQUENCY = 437425000
    DEFAULT_MODINDEX = 1
    DEFAULT_BITRATE = 2400
    DEFAULT_POWER = 26
    DEFAULT_TRAINING = 200
    
    def __init__(self):
        self.bluebox = bluebox.Bluebox()
        self.set_default_config()

    def set_default_config(self):
        self.bluebox.set_frequency(DEFAULT_FREQUENCY)
        self.bluebox.modindex(DEFAULT_MODINDEX)
        self.bluebox.set_bitrate(DEFAULT_BITRATE)
        self.bluebox.set_power(DEFAULT_POWER)
        self.bluebox.set_training(DEFAULT_TRAINING)

    def parser_loop(self):
        while True:
            data, rssi, freq = self.bluebox.receive(10000)
            # Parse data
            packet = self.parse(data)
            # TODO: Report
        
    
    def parse_data(self, data):
        # FEC
        ec = fec.PacketHandler()
        data, bit_corr, byte_corr = ec.deframe(data)
        # Parse CSP
        length = int(binascii.hexlify(data[0:2]), 16)
        header = int(binascii.hexlify(data[2:7]), 16)
        if length > 
        # Parse CSP header
        src = ((header >> 25) & 0x1f)
        dest = ((header >> 20) & 0x1f)
        dest_port = ((header >> 14) & 0x3f)
        src_port = ((header >> 8) & 0x3f)
        
        
