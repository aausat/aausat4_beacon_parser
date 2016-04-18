import predict
import time

def getDoppler(tle, gnd_lat, gnd_lng, gnd_alt, time=time.time()):
    prediction = predict.observe(tle, (gnd_lat, gnd_lng, gnd_alt), time)
    return prediction['doppler']

if __name__ == '__main__':
    from time import sleep, mktime
    from datetime import datetime, timedelta
    tle = """AAUSAT-II               
1 32788U 08021F   16109.53422999  .00001855  00000-0  18309-3 0  9992
2 32788  97.6100 154.3596 0013832 108.1455 252.1273 14.93074504432296"""
    while True:
        doppler = getDoppler(tle, 55.6167, -12.6500, 5)
        raw_input()
        print("time:", start_time)
        print("doppler:", doppler)
        start_time = start_time + timedelta(seconds=1)
        sleep(1)
