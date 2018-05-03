# MAS
MAS stands for Modbus Attack Scripts.

They were developed to assess security level of PLCs and network architectures. It can also be used to test network filtering rules (DPI, Modbus-aware firewalls...).

3 scripts are available now:
- `read_all_holding_registers.py`, used to scan and get values from holding registers on a TCP Modbus Slave;
- `write_all_holding_registers.py`, used to write a specific value to one or multiple holding registers of a TCP Modbus Slave;
- `read_register.py`, used to get values from various types of addresses on a TCP Modbus Slave (Holding Register, Discrete Input, Input Register)


## Prerequisites
```bash
apt-get install python-pip python-dev
pip install pymodbus
```

## read_all_holding_registers.py
```
usage: read_all_holding_registers.py [-h] [-p PORT] [-u UID] [-sa START]
                                      [-ea END]
                                      ip

Read all holding registries from a TCP MODBUS Slave

positional arguments:
  ip                    IP address of the slave

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Modbus Port. Defaults to 502
  -u UID, --uid UID     Modbus Unit ID. Defaults to 1
  -sa START, --start-address START
                        Starting Address for the scanner. Defaults to 1
  -ea END, --end-address END
                        Ending Address for the scanner. Defaults to 65535
```

## write_all_holding_registers.py
```
usage: write_all_holding_registers.py [-h] [-p PORT] [-u UID] [-sa START]
                                      [-ea END] [-v VALUE]
                                      ip

Write all holding registries on a TCP MODBUS Slave

positional arguments:
  ip                    IP address of the slave

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Modbus Port. Defaults to 502
  -u UID, --uid UID     Modbus Unit ID. Defaults to 1
  -sa START, --start-address START
                        Starting Address for the writer. Defaults to 1
  -ea END, --end-address END
                        Ending Address for the writer. Defaults to 65535
  -v VALUE, --value VALUE
                        Value that will be written. Defaults to 7777
```

## read_register.py
```
usage: read_register.py [-h] [-p PORT] [-u UID] [-sa START] [-ea END]
                        [-t TYPE]
                        ip

Read specific addresses on a TCP MODBUS Slave

positional arguments:
  ip                    IP address of the slave

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Modbus Port. Defaults to 502
  -u UID, --uid UID     Modbus Unit ID. Defaults to 1
  -sa START, --start-address START
                        Starting Address for the scanner. Defaults to 1
  -ea END, --end-address END
                        Ending Address for the scanner. Defaults to 65535
  -t TYPE, --type TYPE  Type of Modbus address to read. Values can be 'h' for
                        Holding, 'd' for Discrete Inputs or 'i' for Input
                        Registers. Defaults to 'h'

```
