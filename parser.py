import bluebox, fec, predict
import beacon, config
import binascii, struct
import time, aenum, threading
import argparse
from datetime import datetime

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
    DEFAUL_SYNCWORD = "4f5a34" # OZ4

    LOGFILE = "log.txt"
    
    def __init__(self, qth, config, enable_doppler=True, verify_packets=True):
        self.qth = qth
        self.enable_doppler = enable_doppler
        self.verify_packets = verify_packets
        
        self.center_freq = Parser.DEFAULT_FREQUENCY
        self.bb_lock = threading.Lock()
        with self.bb_lock:
            self.bluebox = bluebox.Bluebox()

        self.config_version = -1
        self.config = config
        self.set_config(self.config.get_config(), True)

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
                    time.sleep(0.01)
                    self.bluebox.set_syncword(int(settings['syncword'], 16)) if 'syncword' in settings else None
                    time.sleep(0.01)
                    
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
                time.sleep(0.01)
                self.bluebox.set_syncword(int(Parser.DEFAULT_SYNCWORD, 16))
                
                self.config_version = -1

    def verify_packet(packet):
        pass
                
    def parse_data(bin_data, verify_packets, logfile=None):
        logmsg = "=================\n"
        logmsg = "{}\n".format(datetime.now().isoformat(' '))
        logmsg += "{}\n".format(binascii.b2a_hex(bin_data))
        payload = None
        if verify_packets:
            resp = Parser.verify_packet(bin_data)
            # print resp['status'] - something linke: payload data from ss to ss
            #                                       : failed verification 
            #                                       : beacon packet
            # if beacon, extract payload

        else:
            # Parsing with verification
            ec = fec.PacketHandler() # for Reed-Solomon codes
            data, bit_corr, byte_corr = ec.deframe(bin_data)
            hexdata = binascii.b2a_hex(data)
            
            logmsg += "{}\n{}, {}\n".format(hexdata, bit_corr, byte_corr)
            # 
            print("\n" + "#="*40 + "#\n")
            print("Received packet {}".format(datetime.now().isoformat(' ')))
            print("Bit corr: {}".format(bit_corr))
            print("Byte corr: {}".format(byte_corr))
            print("{}\n".format(hexdata))
            
            header = struct.unpack("<I", data[0:4])[0]
            # Parse CSP header
            src = ((header >> 25) & 0x1f)
            dest = ((header >> 20) & 0x1f)
            dest_port = ((header >> 14) & 0x3f)
            src_port = ((header >> 8) & 0x3f)
            if CSP_adress(src) == CSP_adress.UHF and CSP_adress(dest) == CSP_adress.MCC and dest_port == 10:
                payload = hexdata[8:-4]
            else:
                print "Possibly payload data from {0} to {1}. Will not attempt to parse".format(CSP_adress(src), CSP_adress(dest))
                return
        
        if payload:
            beacon_decode = beacon.Beacon(payload)
            logmsg += "{}\n".format(beacon_decode)
            print beacon_decode

        if logfile:
            with open(logfile, "a") as f:
                f.write(logmsg)


    def run(self):
        if self.enable_doppler:
            self.__enable_doppler_correction__()

        while True:
            try:
                with self.bb_lock:
                    data, rssi, freq = self.bluebox.receive(1000)
                if data:
                    # Parse data
                    packet = Parser.parse_data(data, self.verify_packets, logfile=Parser.LOGFILE)
                    # TODO: Report
            except Exception as e:
                print e
            # Update config if updated
            # An observer might be more useful
            config = self.config.get_config()
            self.set_config(config)        

    def __enable_doppler_correction__(self):
        qth = (self.qth[0], -self.qth[1], self.qth[2])
        tle = self.config.get_config()['tle']
        self.__doppler_correction__(qth, tle)
        
    def __doppler_correction__(self, qth, tle):
        # the predict library expects long (W)
        # We expect long (E)        
        sat_info = predict.observe(tle, qth)
        freq =  self.center_freq + sat_info['doppler']
        print "Doppler:", freq
        with self.bb_lock:
            self.bluebox.set_frequency(freq)
            
        t = threading.Timer(10, self.__doppler_correction__, [qth, tle])
        t.daemon=True
        t.start()

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='AAUSAT4 Beacon Parser')
    args_parser.add_argument('--lat', dest='lat', required=False, type=float, default=None,
                            help='Latitude of ground station (N), e.g. 55.6167')
    args_parser.add_argument('--lon', dest='lon', required=False, type=float, default=None,
                            help='Longitude of ground station (W), e.g. -12.6500')
    args_parser.add_argument('--alt', dest='alt', required=False, type=float, default=None,
                            help='Altitude of ground station (meters), e.g. 10')
    args_parser.add_argument('--hexstr', dest='hexstr', required=False, default=None,
                            help='Decodes the hex string and exits.')

    args = args_parser.parse_args()

    if args.hexstr:
        Parser.parse_data(args.hexstr, False, False)
        
    elif args.lat and args.lon and args.alt:
        # Start parser
        qth = (args.lat, args.lon, args.alt)
        config = config.Config()
        parser = Parser(qth, config, enable_doppler=False, verify_packets=False)
        parser.run()
    else:
        args_parser.print_help()
        exit(1)
