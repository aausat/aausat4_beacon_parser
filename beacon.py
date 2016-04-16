class EPS:

    def __init__(self, raw_data):
        self.boot_count = None # uint16_t
        self.uptime = None # uint32_t
        self.rt_clock = None # uint32_t
        self.ping_status = None # uint8_t (?)
        self.subsystem_selftatus = None # uint16_t
        self.battery_voltage = None # uint8_t
        self.call_diff = None # int8_t
        self.battery_current = None # int8_t
        self.solar_power = None # uint8_t
        self.temp = None #int8_t
        self.pa_temp = None #int8_t
        self.main_voltage = None #int8_t
        
        print "Missing"

class COM:
    def __init__(self, raw_data):
        self.boot_count = None # uint16_t
        self.packtes_recevied = None # uint16_t
        self.packtes_send = None # uint16_t
        self.latest_rssi = None # uint16_t
        self.latest_bit_correction = None # uint16_t
        self.latest_byte_correction = None # uint16_t
        
        print "Missing"


class Beacon(object):

    def __init__(self, raw_data):
        ## Format:
        #  [ 1 byte | 19 bytes  | 12 bytes | 7 bytes  | 6 bytes  | 20 bytes  | 20 bytes  ]
        #  [ Valid  |    EPS    |    COM   |   ADCS1  |  ADCS2   |   AIS1    |   AIS2    ]
        
        if len(raw_data) != 84:
            raise Exception("Unexpected length (%s)" % len(raw_data))

        valid = raw_data[0]
        eps_raw = raw_data[1:20]
        com_raw = raw_data[20:32]
        adcs1_raw = raw_data[32:39]
        adcs2_raw = raw_data[39:35]
        ais1_raw = raw_data[35:55]
        ais2_raw = raw_data[55:75]

        
        if raw_data[0] & (1 << 0):
            self.eps = EPS(eps_raw)
        print "Missing"


def __lengh_error__(expected, got):
    return 0#Exception("Unexpected length (%s), expected " % (got, expected))
