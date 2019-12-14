#Paul Sanders
#6/26/18
# sniffer_ip_header_decode.py : sniffing tool that decodes the incoming packets (more than sniffer.py)
#TO DO: program works on windows (tested on win7 vm) but ICMP breaks on linux (header sizes not correct)
#
import socket
import os
import struct
from ctypes import *

#host to listen on 
host = "10.50.10.168"

#our IP header
class IP(Structure):
    _fields_ = [
            ("ihl",         c_ubyte, 4),
            ("version",     c_ubyte, 4),
            ("tos",         c_ubyte),
            ("len",         c_ushort),
            ("id",          c_ushort),
            ("offset",      c_ushort),
            ("ttl",         c_ubyte),
            ("protocol_num",c_ubyte),
            ("sum",         c_ushort),
            ("src",         c_ulong),
            ("dst",        c_ulong)
        ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):

        #map protocol consts to proper names
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        #human-readable ip addrs
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))

        #human reabale protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host,0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1 )

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
try:
    while True:

        #read a packet
        raw_buffer = sniffer.recvfrom(65565)[0]

        #create an IP header from first 20 bytes of buffer
        ip_header = IP(raw_buffer[0:20])

        #print out protocol detected &  hosts
        print "Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)

#handle ctrl-c
except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        

