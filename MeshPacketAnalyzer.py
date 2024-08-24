#!/usr/bin/env python3
import argparse
import meshtastic.tcp_interface
from __init__ import VERSION, DEFAULTDEVICE, DEFAULTNODE
from pubsub import pub
from packetAnalyzer import packetAnalyzer
import pytz
import time

USAGE = \
"""
meshpacketanalyzer
"""

DESCRIPTION = \
"""
Decodes and displays all data from all packets received.
"""

EPILOG = \
"""
That is all!
"""

def parseMyArgs():
    parser = argparse.ArgumentParser(\
                    description = DESCRIPTION, usage = USAGE)
    parser.add_argument('-v', '--version', 
                        action='version', 
                        version = VERSION)

    parser.add_argument('-d', '--deviceName',
                                   default = DEFAULTDEVICE,
            help="""Use deviceName as connection to radio. This can be
                    a serial port if connecting via radio USB port, or 
                    the node short name of a WiFi/network connected 
                    node. The available node short names and IP 
                    addresses must be listed in the ipList dictionary 
                    found in file __init__.py. Default is {} if
                    serial==True, or {} if serial == False.""".\
                    format(DEFAULTDEVICE, DEFAULTNODE))

    parser.add_argument('-s', '--serial',
                    default =  False,
                    action = 'store_true',
            help="""The device specified in deviceName is a serial port.
                    """)
    args = parser.parse_args()
    """ Adjust default device name if not a serial port connection."""
    if args.serial == False:
        args.deviceName = DEFAULTNODE
    return args


""" *** Executable Code Starts Here *** """
if __name__ == '__main__':
    args = parseMyArgs()
    print(args)
    mon = packetAnalyzer(node=args.deviceName, serial=args.serial)
    mon.mainLoop()
    """
    interface = meshtastic.tcp_interface.TCPInterface(mon.hostname)
    mon.interface = interface
    #print(f'{type(interface)}\n{dir(interface)}')
    pub.subscribe(mon.onReceive, 'meshtastic.receive')
    pub.subscribe(mon.onConnection, 'meshtastic.connection.established')
    while True: time.sleep(10)
    interface.close()
    """
