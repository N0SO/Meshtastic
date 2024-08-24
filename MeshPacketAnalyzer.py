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
            help="""Use deviceName as serial input device.
                    default is {}""".format(DEFAULTDEVICE))

    parser.add_argument('-n', '--nodeName',
                    default =  DEFAULTNODE,
            help="""Use nodeName as default IP node. Default is {}"""\
                    .format(DEFAULTNODE))
    args = parser.parse_args()
    return args


""" *** Executable Code Starts Here *** """
if __name__ == '__main__':
    args = parseMyArgs()
    mon = packetAnalyzer(node=args.nodeName, serial=args.deviceName)
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
