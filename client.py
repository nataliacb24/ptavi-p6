#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


if len(sys.argv) == 3:
    Method = sys.argv[1]
    Login = sys.argv[2]
    try:
        (receptor, port) = Login.split(':')
        port = int(port)
        (name, IP) = receptor.split('@')
    except ValueError:
         sys.exit("Usage: python client.py method receiver@IP:SIPport")
else:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, port))

Peticion_SIP = Method + " " + "sip:" + name + "@" + IP + " " + "SIP/2.0"
print("Enviando: " + Peticion_SIP)
my_socket.send(bytes(Peticion_SIP, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
datos = data.decode('utf-8').split()
if datos[1] == "100" and datos[4] == "180" and datos[7] == "200":
    Peticion_SIP = "ACK sip:" + name + "@" + IP + " SIP/2.0" + "\r\n"
    my_socket.send(bytes(Peticion_SIP, 'utf-8') + b'\r\n')
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
