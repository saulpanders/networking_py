#Paul Sanders
#6/26/18
# sniffer.py : a simple UDP packet sniffer (single packet)

import socket
import os

#host to listen on (if unsure, run ifconfig and get the broadcast ip)
host = "10.50.10.168"

#create raw socket and bind it to public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host,0))

#include ip headers in capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)

#if were on Windows, need to send an IOCTL (to set up promiscuous mode)
if os.name == "nt":
    sniffer.ioctl(SOCKET.SIO_RCVALL, socket.RCVALL_ON)

print sniffer.recvfrom(65565)

#if were on Windows, turn off promiscuous mode
if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

