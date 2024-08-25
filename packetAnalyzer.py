# This program connects to a local Meshtastic node (via WiFi)
# and displays the contents of all packets received.
#
# The ipList dictionary must be edited to reflect the ShortName
# and IP address of your Meshtastic nodes.
#
import meshtastic.tcp_interface, meshtastic.serial_interface
from __init__ import ipList, VERSION
from meshtastic import mesh_pb2, storeforward_pb2, paxcount_pb2, BROADCAST_NUM
from pubsub import pub
from datetime import datetime
import pytz
import time
#
# Edit ipList as needed for your local nodes
#
"""
ipList moved to __init__.py
Need to add option to use serial interface in addition to IP.
"""
class packetAnalyzer():
    def __init__(self, node = None, serial = None, interface = None):
        self.node = node
        self.serial = serial
        self.interface = interface
        self.hostname = None
        if serial:
            self.hostname = node
        else:
            ip_num = ipList.get(node, "None")
            if ip_num:
                self.hostname = ip_num
            else: 
                print (f"> Node {node} not found. \n>")
                exit()            

        #print(f'{self.node}\n{self.serial}')
                 
    def PrintIpList(self):
        for name, ip in ipList.items():
            print (name)
            
    def GetLocalNode(self):
        valid = False
        while valid == False:
            print ("* Connect to Local Node *")
            print ("* Type ? for options    *")
            print ("> Enter Local Node Name:")
            text = input("> ")
            if text == '?': PrintIpList()
            else:
                ip_num = ipList.get(text, "None")
                if ip_num == "None": print ("> Node not found \n>")
                else: valid = True
        self.node = text
        self.ip_num = ip_num
        print ("> Success!")
        print ("> Connected to:",self.node)
        print ("-------------------------------")
        return ip_num       

    def idToHex(self, nodeId): return '!' + hex(nodeId)[2:]

    def GetCurrentTime(self):
        tz = pytz.timezone('US/Pacific')
        now_tz = tz.localize(datetime.now())
        now_str = now_tz.strftime("%Y-%m-%d %I:%M:%S %p")
        return now_str

    def GetNodeName(self, node_id):
        node_name = hex(node_id)
        hex_id = '!' + hex(node_id)[2:]
        for node in self.interface.nodes.values():
            if hex_id == node["user"]["id"]:
                node_name = node["user"]["longName"]
        return  node_name
        
    def getVersion(self):
        return VERSION
        
    def onConnection(self, interface, topic=pub.AUTO_TOPIC):
        print ("> Mesh Packet Monitor Program")
        print (f"> Version {self.getVersion()}")
        print ("> Connected to " + self.GetNodeName(interface.myInfo.my_node_num))
        print (">", self.GetCurrentTime())
        print ("-------------------------------")

    def onReceive(self, packet, interface):
        # Print all packets
        #print(f"{packet} \n\n") 
        print("Received packet:")
        print("  Time:", self.GetCurrentTime())
        print("  From:", self.GetNodeName(packet['from']))
        if packet['to'] != 0xffffffff:
            print("    To: ", self.GetNodeName(packet['to']))
        if 'hopStart' in packet:
            print(f"  Hop Start: {packet['hopStart']}")
        if 'hopLimit' in packet:
            print(f"  Hop Limit: {packet['hopLimit']}")
        if 'rxSnr' in packet:
            print(f"  SNR: {packet['rxSnr']}")
        if 'rxRssi' in packet:
            print(f"  RSSI: {packet['rxRssi']}")
        if 'decoded' in packet:
            print(f"  Port Number: {packet['decoded'].get('portnum', 'N/A')}")
            if packet['decoded'].get('portnum') == 'NODEINFO_APP':
                print("  Node Information:")
                node_info = packet['decoded'].get('user', {})
                print(f"    ID: {node_info.get('id', 'N/A')}")
                print(f"    Long Name: {node_info.get('longName', 'N/A')}")
                print(f"    Short Name: {node_info.get('shortName', 'N/A')}")
                print(f"    MAC Address: {node_info.get('macaddr', 'N/A')}")
                print(f"    Hardware Model: {node_info.get('hwModel', 'N/A')}")
                if 'role' in packet:
                    print(f"    Role: {node_info.get('role', 'N/A')}")
                if 'isLicensed' in packet:
                    print(f"    Role: {node_info.get('isLicensed', 'N/A')}")

            elif packet['decoded'].get('portnum') == 'POSITION_APP':
                print("  Position:")
                position = packet['decoded']['position']
                print(f"    Latitude: {position.get('latitude', 'N/A')}")
                print(f"    Longitude: {position.get('longitude', 'N/A')}")
                print(f"    Altitude: {position.get('altitude', 'N/A')}")
                if 'PDOP' in position:
                    print(f"    PDOP: {position.get('PDOP', 'N/A')}")
                if 'ground_track' in position:
                    print(f"    Ground Track: {position.get('ground_track', 'N/A')}")
                if 'sats_in_view:' in position:
                    print(f"    Satellites in View: {position.get('sats_in_view:', 'N/A')}")

            elif packet['decoded'].get('portnum') == 'TEXT_MESSAGE_APP':
                print("  Text Message:")
                print(f"    Text: {packet['decoded']['text']}")

            elif packet['decoded'].get('portnum') == 'TELEMETRY_APP':
                print("  Telemetry:")
                telemetry = packet['decoded'].get('telemetry', {})
                print(f"    Time: {telemetry.get('time', 'N/A')}")
                print("    Device Metrics:")
                device_metrics = telemetry.get('deviceMetrics', {})
                if device_metrics:
                    print(f"      Battery Level: {device_metrics.get('batteryLevel', 'N/A')}")
                    print(f"      Voltage: {device_metrics.get('voltage', 'N/A')}")
                    print(f"      Channel Utilization: {device_metrics.get('channelUtilization', 'N/A')}")
                    print(f"      Air Utilization Tx: {device_metrics.get('airUtilTx', 'N/A')}")
                power_metrics = telemetry.get('powerMetrics', {})
                if power_metrics:
                    print("    Power Metrics:")
                    print(f"      CH1 Voltage: {power_metrics.get('ch1Voltage', 'N/A')}")
                    print(f"      CH1 Current: {power_metrics.get('ch1Current', 'N/A')}")
                    print(f"      CH2 Voltage: {power_metrics.get('ch2Voltage', 'N/A')}")
                    print(f"      CH2 Current: {power_metrics.get('ch2Current', 'N/A')}")
                    print(f"      CH3 Voltage: {power_metrics.get('ch3Voltage', 'N/A')}")
                    print(f"      CH3 Current: {power_metrics.get('ch3Current', 'N/A')}")
                    print(f"      CH4 Voltage: {power_metrics.get('ch4Voltage', 'N/A')}")
                    print(f"      CH4 Current: {power_metrics.get('ch4Current', 'N/A')}")
                environment_metrics = telemetry.get('environmentMetrics', {})
                if environment_metrics:
                    print("    Environment Metrics:")
                    print(f"      Temperature: {environment_metrics.get('temperature', 'N/A')}")
                    print(f"      Relative Humidity: {environment_metrics.get('relativeHumidity', 'N/A')}")
                    print(f"      Barometric Pressure: {environment_metrics.get('barometricPressure', 'N/A')}")
                    print(f"      Air Quality (IQA Resistance): {environment_metrics.get('gasResistance', 'N/A')}")

            elif packet['decoded'].get('portnum') == 'NEIGHBORINFO_APP':
                # Neighbor Information
                print("  Neighbor Information:")
                message = mesh_pb2.NeighborInfo()
                payload_bytes = packet['decoded'].get('payload', b'')
                message.ParseFromString(payload_bytes)
                print(f"    Node ID: {message.node_id} / {idToHex(message.node_id)}")
                print(f"    Last Sent By ID: {message.last_sent_by_id}")
                print(f"    Node Broadcast Interval (secs): {message.node_broadcast_interval_secs}")
                print("    Neighbors:")
                for neighbor in message.neighbors:
                    print(f"      Neighbor ID: {neighbor.node_id} / {idToHex(neighbor.node_id)}")
                    print(f"        SNR: {neighbor.snr}")

            elif packet['decoded'].get('portnum') == 'RANGE_TEST_APP':
                print("  Range Test Information:")
                payload = packet['decoded'].get('payload', b'')
                print(f"    Payload: {payload.decode()}")
            
            elif packet['decoded'].get('portnum') == 'STORE_FORWARD_APP':
                print("  Store Forward Information:")
                message = storeforward_pb2.StoreAndForward()
                payload_bytes = packet['decoded'].get('payload', b'')
                message.ParseFromString(payload_bytes)
                if message.HasField('stats'):
                    print(f"    Statistics: {message.stats}")
                if message.HasField('history'):
                    print(f"    History: {message.history}")
                if message.HasField('heartbeat'):
                    print(f"    Heartbeat: {message.heartbeat}")

            elif packet['decoded'].get('portnum') == 'ADMIN_APP':
                print("  Administrative Information:")
                payload = packet['decoded'].get('payload', b'')
                print(f"    Payload: {payload}")
                admin_info = packet['decoded'].get('admin', {})
                if 'getChannelResponse' in admin_info:
                    response = admin_info['getChannelResponse']
                    print("    Get Channel Response:")
                    print(f"      Index: {response.get('index', 'N/A')}")
                    print("      Settings:")
                    settings = response.get('settings', {})
                    for key, value in settings.items():
                        print(f"        {key}: {value}")

            elif packet['decoded'].get('portnum') == 'PAXCOUNTER_APP':
                print("  Paxcounter Information:")
                message = paxcount_pb2.Paxcount()
                payload_bytes = packet['decoded'].get('payload', b'')
                message.ParseFromString(payload_bytes)
                print(f"    Wifi: {message.wifi}")
                print(f"    BLE: {message.ble}")
                print(f"    Uptime: {message.uptime}")
                
            else:
                print(f"  Decoded packet does not contain data we are looking for!")
        else:
            print("  Encrypted packet and we don't have the key!")
        print()
        
    def mainLoop(self):
        if self.serial:
            print(f'Opening serial port {self.hostname}')
            self.interface = meshtastic.serial_interface.SerialInterface(self.hostname)            
        else:
            print(f'Opening TCPIP {self.hostname}')
            self.interface = meshtastic.tcp_interface.TCPInterface(self.hostname)
        pub.subscribe(self.onReceive, 'meshtastic.receive')
        pub.subscribe(self.onConnection, 'meshtastic.connection.established')

        while True: 
            time.sleep(10)
            
        interface.close()

