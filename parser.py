import bluebox, fec
import beacon, config
import binascii, struct
import time, aenum, threading

class CSP_adress(aenum.Enum):
    ESP   = 0
    FP    = 1
    LOG   = 1
    SWISS = 1
    AIS2  = 3
    UHF   = 4
    ADCS1 = 5
    ADCS2 = 6
    MCC   = 9

class Parser(threading.Thread):

    DEFAULT_FREQUENCY = 437425000
    DEFAULT_MODINDEX = 1
    DEFAULT_BITRATE = 2400
    DEFAULT_POWER = 26
    DEFAULT_TRAINING = 200
    
    def __init__(self, qth, config, enable_doppler=True, verify_packets=True):
        self.qth = qth
        self.enable_doppler = enable_doppler
        self.verify_packets = verify_packets
        
        self.center_freq = Parser.DEFAULT_FREQUENCY
        self.bb_lock = threading.Lock()
        with self.bb_lock:
            self.bluebox = bluebox.Bluebox()

        self.config_version = -1            
        self.set_config(config, True)

    def set_config(self, config, force_update=False):
        with self.bb_lock:
            if config:
                if force_update or ('version' in config and config['version'] > self.config_version):
                    settings = config['radio_settings']
                    self.center_freq = settings['frequency'] if 'frequency' in settings else DEFAULT_FREQUENCY
                    
                    self.bluebox.set_frequency(self.center_freq)
                    time.sleep(0.01)
                    self.bluebox.set_modindex(settings['modindex']) if 'modindex' in settings else None
                    time.sleep(0.01)
                    self.bluebox.set_bitrate(settings['bitrate']) if 'bitrate' in settings else None
                    time.sleep(0.01)
                    self.bluebox.set_power(settings['power']) if 'power' in settings else None
                    time.sleep(0.01)
                    self.bluebox.set_training(settings['training']) if 'training' in settings else None
                    self.config_version = config['version'] if 'version' in config else self.config_version
                
            elif force_update:
                # Set default config
                self.bluebox.set_frequency(Parser.DEFAULT_FREQUENCY)
                time.sleep(0.01)
                self.bluebox.set_modindex(Parser.DEFAULT_MODINDEX)
                time.sleep(0.01)
                self.bluebox.set_bitrate(Parser.DEFAULT_BITRATE)
                time.sleep(0.01)
                self.bluebox.set_power(Parser.DEFAULT_POWER)
                time.sleep(0.01)
                self.bluebox.set_training(Parser.DEFAULT_TRAINING)

    def verify_pakcet(self, packet):
        pass
                
    def parse_data(self, bin_data, verify_packets):
        if verify_packets:
            resp = verify_pakcet(bin_data)
            # print resp['status'] - something linke: payload data from ss to ss
            #                                       : failed verification 
            #                                       : beacon packet
            # if beacon, extract payload

        else:
            # Parsing with verification
            ec = fec.PacketHandler() # for Reed-Solomon codes
            data, bit_corr, byte_corr = ec.deframe(bin_data)
            # 
            header = struct.unpack("<I", data[0:4])[0]
            # Parse CSP header
            src = ((header >> 25) & 0x1f)
            dest = ((header >> 20) & 0x1f)
            dest_port = ((header >> 14) & 0x3f)
            src_port = ((header >> 8) & 0x3f)

            if src == CSP_adress.UHF and dest == CSP_adress.MCC and dest_port == 42:
                data = binascii.b2a_hex(data)
                payload = data[8:-4]
            else:
                return
                
        print beacon.Beacon(payload)


    def run(self):
        if self.enable_doppler:
            self.__enable_doppler_correction__()

        while True:
            try:
                with self.bb_lock:
                    data, rssi, freq = self.bluebox.receive(1000)
                if data:
                    # Parse data
                    packet = self.parse_data(data, self.verify_packets)
                    # TODO: Report
            except Exception as e:
                print e
            # Update config if updated
            # An observer might be more useful
            config = self.config.get_config()
            self.set_config(config)        

    def __enable_doppler_correction__(self):
        def doppler_correction(self):
            # the predict library expects long (W)
            # We expect long (E)
            qth = self.qth
            qth[1] = -qth[1]
            
            sat_info = predict.observe(tle, qth)

            with self.bb_lock:
                self.bluebox.set_frequency(self.center_freq + sat_info['doppler'])

        t = threading.Timer(1, doppler_correction, ())
        t.daemon=True
        t.start()
            
if __name__ == '__main__':
    qth = (55.6167, -12.6500, 5) # AAU
    config = config.Config()
    parser = Parser(qth, config)
    parser.run()
