from openrtist_engine import OpenrtistEngine
import time


class TimingEngine(OpenrtistEngine):
    def __init__(self, compression_params, adapter):
        super().__init__(compression_params, adapter)
        self.count = 0
        self.lasttime = time.time()
        self.lastcount = 0
        self.lastprint = self.lasttime

    def handle(self, from_client):
        self.t0 = time.time()
        result = super().handle(from_client)
        self.t3 = time.time()

        self.count += 1
        if (self.t3 - self.lastprint > 5):
            print('pre {0:.1f} ms, '.format(
                (self.t1-self.t0)*1000), end='')
            print('infer {0:.1f} ms, '.format(
                (self.t2-self.t1)*1000), end='')
            print('post {0:.1f} ms, '.format(
                (self.t3-self.t2)*1000), end='')
            print('wait {0:.1f} ms, '.format(
                (self.t0-self.lasttime)*1000), end='')
            print('fps {0:.2f}'.format(
                1.0/(self.t3-self.lasttime)))
            print('avg fps: {0:.2f}'.format(
                  (self.count-self.lastcount)/(self.t3-self.lastprint)))
            print()
            self.lastcount = self.count
            self.lastprint = self.t3

        self.lasttime = self.t3

        return result

    def inference(self, preprocessed):
        self.t1 = time.time()
        result = super().inference(preprocessed)
        self.t2 = time.time()

        return result