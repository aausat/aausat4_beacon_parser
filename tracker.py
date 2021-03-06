import predict
import time

class Tracker:

    def __init__(self, qth, tle, center_freq):
        self.qth = qth
        self.tle = tle
        self.freq = center_freq
        
    def set_center_frequncy(self, center_freq):
        self.freq = center_freq

    
    def get_doppler(self, obs_time=None):
        if not obs_time:
            obs_time = time.time()
        prediction = predict.observe(self.tle, self.qth, obs_time)
        doppler = prediction['doppler']
        correction = (self.freq/100E6) * doppler
        return correction

    def in_range(self, obs_time=None):
        if not obs_time:
            obs_time = time.time()

        if self.get_elevation(obs_time) > 0:
            return True
        else:
            return False

    def next_pass(self, obs_time=None):
        if not obs_time:
            obs_time = time.time()

        p = predict.transits(self.tle, self.qth, ending_after=obs_time)
        transit = p.next()
        return transit.start, transit.duration(), transit.peak()['elevation']
        
    def get_elevation(self, obs_time=None):
        if not obs_time:
            obs_time = time.time()

        prediction = predict.observe(self.tle, self.qth, obs_time)
        return prediction['elevation']

    def get_azimuth(self, obs_time=None):
        if not obs_time:
            obs_time = time.time()

        prediction = predict.observe(self.tle, self.qth, obs_time)
        return prediction['azimuth']

if __name__ == '__main__':
    tle = """AAUSAT-II               
1 32788U 08021F   16109.53422999  .00001855  00000-0  18309-3 0  9992
2 32788  97.6100 154.3596 0013832 108.1455 252.1273 14.93074504432296"""
    qth = (55.6167, -12.6500, 5)

    tracker = Tracker(qth, tle, 437.425e6)

    print tracker.in_range()
    print tracker.next_pass()
    print tracker.get_elevation()
    print tracker.get_azimuth()
    print tracker.get_doppler()
