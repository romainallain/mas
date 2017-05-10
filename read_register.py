#!/usr/bin/env python

"""
File: read_register.py
Desc: Read specific registers from a TCP MODBUS Slave
Version: 0.0.1
"""

__author__ = 'rm'

from pymodbus.client.sync import ModbusTcpClient
import argparse
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

def validate_mbaddrtype(s):
    addrtype_set = ("h", "d", "i")
    return s in addrtype_set

def read_holding(addr, client, uid):
    req = client.read_holding_registers(addr, 1, unit=uid)
    return req

def read_discrete(addr, client, uid):
    req = client.read_discrete_inputs(addr, 1, unit=uid)
    return req

def read_inputregister(addr, client, uid):
    req = client.read_input_registers(addr, 1, unit=uid)
    return req

def scan():
    parser = argparse.ArgumentParser(description = "Read specific addresses on a TCP MODBUS Slave")
    parser.add_argument("ip", help="IP address of the slave")
    parser.add_argument("-p", "--port", dest="port", help="Modbus Port. Defaults to 502", type=int, metavar="PORT", default=502)
    parser.add_argument("-u", "--uid", dest="uid", help="Modbus Unit ID. Defaults to 1", type=int, metavar="UID", default=1)
    parser.add_argument("-sa", "--start-address", dest="start_address", help="Starting Address for the scanner. Defaults to 1", type=int, metavar="START", default=1)
    parser.add_argument("-ea", "--end-address", dest="end_address", help="Ending Address for the scanner. Defaults to 65535", type=int, metavar="END", default=65535)
    parser.add_argument("-t", "--type", dest="register_type", help="Type of Modbus address to read. Values can be 'h' for Holding, 'd' for Discrete Inputs or 'i' for Input Registers. Defaults to 'h'", type=str, metavar="TYPE", default="h")
    
    args = parser.parse_args()
    
    try:
        ip = args.ip
    except IndexError:
        print "ERROR: No target to scan\n\n"
        parser.print_help()
        exit()

    # ip address format verification
    if not validate_ipv4(ip):
        print "ERROR: IP address is invalid\n\n"
        parser.print_help()
        exit()

    # modbus address type verification
    if not validate_mbaddrtype(args.register_type):
        print "ERROR: Invalid Modbus address type\n\n"
        parser.print_help()
        exit()

    print 'Connecting to %s...' % ip,
    # connect to modbus slave
    client = ModbusTcpClient(ip, args.port)
    client.connect()
    if client.socket == None:
        print "ERROR: Could not connect to %s." %ip
        exit()
    print ' Connected.'

    # TODO add ETA mechanism
    results = {}
    addr = 1
    readfunction = {
        "h": read_holding,
        "d": read_discrete,
        "i": read_inputregister
    }
    registers_tested = args.end_address - args.start_address + 1
    if registers_tested == 1:
        hr = readfunction[args.register_type](args.start_address, client, args.uid)
        #hr = client.read_holding_registers(args.start_address, 1, unit=args.uid) # unit value is device id of the slave (UID)
        if hr.function_code == 3: # if we succeed reading stuff
            results[addr] = hr.registers[0]
        # if it fails, hr.function = 131 (0x83), cf modbus doc
    else:
    	for addr in range(args.start_address, args.end_address):
            hr = readfunction[args.register_type](addr, client, args.uid)
            #hr = client.read_holding_registers(addr, 1, unit=args.uid) # unit value is device id of the slave (UID)
            if hr.function_code == 3: # if we succeed reading stuff
                results[addr] = hr.registers[0]
            # if it fails, hr.function = 131 (0x83), cf modbus doc

    client.close()
    print 'Register scanning is finished (%d registers were tried)' % (registers_tested)
    # sorting dict for printing
    ordered_results = collections.OrderedDict(sorted(results.items()))
    for addr, value in ordered_results.iteritems():
        print 'Addr {0} \t{1}'.format(addr,value)

if __name__=="__main__":
    try:
        scan()
    except KeyboardInterrupt:
        status("Ctrl-C happened\n")
