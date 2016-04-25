# AAUSAT4 Beacon Parser

Software for parsing AAUSAT4 beacons using a bluebox.

Installation:
```
$ git clone https://github.com/aausat/aausat4_beacon_parser.git
$ pip install -r requirements.txt
```

```
$ python bb_frontend.py -h
usage: bb_frontend.py [-h] [--lat LAT] [--lon LON] [--alt ALT]
                      [--disable-tracking] [--enable-authentication]
                      [--config-file CONFIG_FILE]

AAUSAT4 Bluebox based Beacon Parser

optional arguments:
  -h, --help            show this help message and exit
  --lat LAT             Latitude of ground station (N), e.g. 55.6167
  --lon LON             Longitude of ground station (W), e.g. -12.6500
  --alt ALT             Altitude of ground station (meters), e.g. 10
  --disable-tracking    Disables doppler correction and pass planning.
  --enable-authentication
                        Enables automatic reporting of received packets.
  --config-file CONFIG_FILE
                        Use a confguration file from the local disk instead of
                        the one provided by AAUSAT (on github).

```

When start the program for continuous decoding (with a BlueBox),
the location of the ground station is specified as arguments when the
program is started (or the `--disable-tracking` flag).
The location is used for doppler tracking.

If the `--enable-authentication` flag is specified, all raw data will be
forwarded to the AAUSAT4 team. In the future will a status of the packet 
be returned, indicating validity of the packet

```
$ python parser.py --lat 55.6167 --lon -12.6500 --alt 10 --enable-authentication
```


