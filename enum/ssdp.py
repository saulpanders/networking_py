#inspired by https://github.com/crquan/work-on-sony-apis/blob/master/search-nex.py

import sys
import socket
import argparse

SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900
SSDP_MX = 1
SSDP_ST = "urn:dial-multiscreen-org:service:dial:1"
#SSDP_ST = "urn:schemas-kinoma-com:device:shell:1"
#ST: urn:schemas-kinoma-com:device:shell:1

ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
        "HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT) + \
                "MAN: \"ssdp:discover\"\r\n" + \
                "MX: %d\r\n" % (SSDP_MX, ) + \
                "ST: %s\r\n" % (SSDP_ST, ) + "\r\n"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(ssdpRequest.encode('utf-8'), (SSDP_ADDR, SSDP_PORT))
sock.settimeout(2)

while True:
    try:
        data = sock.recv(1024)
        parse = data.decode('utf-8').split('\r\n')
        print(data)
        print(parse)
    except:
        break

print("ALL DISCOVERED")



