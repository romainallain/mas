#!/usr/bin/env python

"""
File: read_all_holding_registries.py
Desc: Read all holding registries from a TCP MODBUS Slave
Version: 0.0.1
"""

__author__ = 'rm'

from optparse import OptionParser
from pymodbus.client.sync import ModbusTcpClient
import sys
import collections


class ModbusException(Exception):
    _codes = {
        1:  'ILLEGAL FUNCTION',
        2:  'ILLEGAL DATA ADDRESS',
        3:  'ILLEGAL DATA VALUE',
        4:  'SLAVE DEVICE FAILURE',
        6:  'SLAVE DEVICE BUSY'
    }

    def __init__(self, code):
        self.code = code
        self.message = ModbusException._codes[code] if ModbusException._codes.has_key(code) else 'Unknown Modbus Exception'

    def __str__(self):
        return "Modbus Error. Exception %d: %s" % (self.code, self.message)


def status(msg):
    sys.stderr.write(msg[:-1][:39].ljust(39,' ')+msg[-1:])

def validate_ipv4(s):
    pieces = s.split('.')
    if len(pieces) != 4: return False
    try: return all(0<=int(p)<256 for p in pieces)
    except ValueError: return False

def scan(argv):
    
    # TODO add start/stop addr mechanism
    parser = OptionParser(
        usage = "usage: %prog [options] [ip address]",
        description = """Read all holding registries from a TCP MODBUS Slave""")
    parser.add_option("--port", dest="port", help="Modbus port", type="int", metavar="PORT", default="502")
    parser.add_option("--uid", dest="uid", help="Modbus Unit ID", type="int", metavar="UID", default="1")
    
    (options, args) = parser.parse_args(argv)
    
    try:
        ip = args[0]
    except IndexError:
        print "ERROR: No target to scan\n\n"
        parser.print_help()
        exit()

    # ip address format verification
    if not validate_ipv4(ip):
        print "ERROR: IP address is invalid\n\n"
        parser.print_help()
        exit()

    print 'Connecting to %s...' % ip,
    # connect to modbus slave
    client = ModbusTcpClient(ip, options.port)
    client.connect()
    if client.socket == None:
        print "ERROR: Could not connect to %s." %ip
        exit()
    print ' Connected.'

    # TODO add ETA mechanism
    results = {}
    addr = 1
    for addr in range(1, 65535):
        hr = client.read_holding_registers(addr, 1, unit=options.uid) # unit value is device id of the slave (UID)
        if hr.function_code == 3: # if we succeed reading stuff
            results[addr] = hr.registers[0]
        # if it fails, hr.function = 131 (0x83), cf modbus doc

    client.close()
    print 'Register scanning is finished (65535 registers were tried)' # TODO add stop-start+1
    # sorting dict for printing
    ordered_results = collections.OrderedDict(sorted(results.items()))
    for addr, value in ordered_results.iteritems():
        print 'Addr {0} \t{1}'.format(addr,value)

if __name__=="__main__":
    try:
        scan(sys.argv[1:])
    except KeyboardInterrupt:
        status("Ctrl-C happened\n")
