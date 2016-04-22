import bluebox, fec
import config, parser
import threading
import argparse
from datetime import datetime

class bb_frontend(threading.Thread):

    DEFAULT_FREQUENCY = 437425000
    DEFAULT_MODINDEX = 1
    DEFAULT_BITRATE = 2400
    DEFAULT_POWER = 26
    DEFAULT_TRAINING = 200
    DEFAUL_SYNCWORD = "4f5a34" # OZ4
    LOGFILE = "log.txt"
    
    def __init__(self, conf, enable_tracking=False):
        self.conf = conf
        self.enable_tracking = enable_tracking
        self.bluebox = bluebox.Bluebox()
        self.parser = parser.Parser()
        
        if(self.enable_tracking):
            self.tracker = tracker.Tracker(qth, tle)

    def run(self):
        if self.enable_tracking:
            self.__run_pass__()
        else:
            self.__receive_mode__()
            # Update config if updated
            # An observer might be more useful
            #config = self.config.get_config()
            #self.set_config(config)

    def __run_pass__(self):
        while self.tracker.in_range():
            pass

    def __receive_mode__(self):
        while True:
            try:
                data, rssi, freq = self.bluebox.receive(1000)
                if data:
                    print("\n" + "#="*40 + "#\n")
                    print("Received packet {}".format(datetime.now().isoformat(' ')))
                    print("{}\n".format(data))

                    # Parse data
                    try:
                        beacon_str = self.parser.parse_data(data)
                    except Exception as e:
                        print e
                    else:
                        print beacon_str
                        # TODO: Report
            except Exception as e:
                print e



if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='AAUSAT4 Beacon Parser')
    args_parser.add_argument('--lat', dest='lat', required=False, type=float, default=None,
                            help='Latitude of ground station (N), e.g. 55.6167')
    args_parser.add_argument('--lon', dest='lon', required=False, type=float, default=None,
                            help='Longitude of ground station (W), e.g. -12.6500')
    args_parser.add_argument('--alt', dest='alt', required=False, type=float, default=None,
                            help='Altitude of ground station (meters), e.g. 10')
    args_parser.add_argument('--disable-doppler', dest='enable_doppler',
                             action='store_false',
                             required=False,
                             help='Disables doppler tracking.')
    args_parser.add_argument('--enable-reporting', dest='enable_reporting',
                             action='store_true',
                             required=False,
                             help='Enables automatic reporting of received packets.')

    args = args_parser.parse_args()
        
    if (not args.enable_doppler) or (args.lat and args.lon and args.alt):
        # Start parser
        qth = None
        if args.enable_doppler:
            qth = (args.lat, args.lon, args.alt)
        config = config.Config()
        bb_frontend(None).run()
        
    else:
        args_parser.print_help()
        exit(1)
