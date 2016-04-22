# AAUSAT4 Beacon Parser

Software for parsing AAUSAT4 beacons using a bluebox.

Installation:
```
$ git clone https://github.com/aausat/aausat4_beacon_parser.git
$ pip install -r requirements.txt
```

```
$ python parser.py -h
usage: parser.py [-h] [--lat LAT] [--lon LON] [--alt ALT] [--disable-doppler]
                 [--enable-reporting] [--hexstr HEXSTR]

AAUSAT4 Beacon Parser

optional arguments:
  -h, --help          show this help message and exit
  --lat LAT           Latitude of ground station (N), e.g. 55.6167
  --lon LON           Longitude of ground station (W), e.g. -12.6500
  --alt ALT           Altitude of ground station (meters), e.g. 10
  --disable-doppler   Disables doppler tracking.
  --enable-reporting  Enables automatic reporting of received packets.
  --hexstr HEXSTR     Decodes the hex string and exits.
```

When start the program for continuous decoding (with a BlueBox),
the location of the ground station is specified as arguments when the
program is started (or the `--disable-doppler` flag).
The location is used for doppler tracking.

If the `--enable-reporting` flag is specified, all raw data will be
forwarded to the AAUSAT4 team.

```
$ python parser.py --lat 55.6167 --lon -12.6500 --alt 10 --enable-reporting
```


