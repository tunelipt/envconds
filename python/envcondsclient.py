import numpy as np
import xmlrpc.client


class EnvCondsClient(object):

    def __init__(self, ip='localhost', port=9539):

        self.dev = xmlrpc.client.ServerProxy("http://{}:{}".format(ip, port))

    def press(self):
        return self.dev.press()
    def presstemp(self):
        return self.dev.presstemp()
    def humidity(self):
        return self.dev.humidity()
    def humtemp(self):
        return self.dev.humtemp()
    def temp(self, i=1):
        if (i < 1 or i > 5):
            error("Only temperature sensors 1-5 are available")
            return
        return self.dev.temp(i)
    def status(self):
        return self.dev.status()
    
    
