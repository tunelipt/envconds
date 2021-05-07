

import serial
import time
import argparse

from xmlrpc.server import SimpleXMLRPCServer


class EnvConds(object):

    def __init__(self, comport='/dev/ttyUSB0', baud=9600, timeout=2):

        self.dev = serial.Serial(comport, baud, timeout=timeout);
    def open(self):
        if self.dev.is_open:
            self.dev.close()
        self.dev.open()
        self.dev.flushInput()
        self.dev.flushOutput()
        time.sleep(0.1)
    def close(self):
        self.flush()
        self.dev.close()
        
    def flush(self):
        self.dev.flushInput()
        self.dev.flushOutput()
        
    def press(self):
        cmd = b'*PP'
        self.dev.write(cmd)
        self.dev.flushOutput()
        time.sleep(0.1)
        s = self.dev.readline()
        time.sleep(0.1)
        return float(s)
    
    def presstemp(self):
        cmd = b'*PT'
        self.dev.write(cmd)
        self.dev.flushOutput()
        time.sleep(0.1)
        s = self.dev.readline()
        time.sleep(0.1)
        return float(s)
    
    def humidity(self):
        cmd = b'*HH'
        self.dev.write(cmd)
        self.dev.flushOutput()
        time.sleep(0.1)
        s = self.dev.readline()
        time.sleep(0.1)
        return float(s)
    
    def humtemp(self):
        cmd = b'*HT'
        self.dev.write(cmd)
        self.dev.flushOutput()
        time.sleep(0.1)
        s = self.dev.readline()
        return float(s)
    
    def temp(self, i=1):
        if (i < 1 or i > 5):
            error("Only temperature sensors 1-5 are available")
            return
        i = int(i)
        cmd = "*T{}".format(i).encode('ascii')
        self.dev.write(cmd)
        self.dev.flushOutput()
        time.sleep(0.1)
        s = self.dev.readline()
        time.sleep(0.1)
        return float(s)

    def clear(self):
        cmd = b'%'
        self.dev.write(cmd)
        self.dev.flushOutput()
        time.sleep(0.1)
        return
    
    def status(self):
        cmd = b'*S1'
        self.dev.write(cmd)
        self.dev.flushOutput()
        time.sleep(0.1)
        s = self.dev.readline()
        time.sleep(0.1)
        return s
    


def start_server(ip='localhost', port=9541, comport='/dev/ttyUSB0', baud=115200):
    dev = ESPDaq(comport, baud)
    print("Starting XML-RPC server")
    print("IP: {}, port: {}".format(ip, port))
    server = SimpleXMLRPCServer((ip, port), allow_none=True)
    server.register_instance(dev)
    server.serve_forever()


if __name__ == "__main__":
    print("Creating interface ...")
    parser = argparse.ArgumentParser(description="ESPDaq server")
    parser.add_argument("-i", "--ip", help="IP address of the XML-RPC server", default="localhost")
    parser.add_argument("-p", "--port", help="XML-RPC server port", default=9541, type=int)
    parser.add_argument("-s", "--comport", help="Serial port to be used", default="/dev/ttyUSB0")

    args = parser.parse_args()
    start_server(args.ip, args.port, args.comport)
    
    
