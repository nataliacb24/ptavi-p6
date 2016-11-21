#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()      
            Peticion_SIP = line.decode('utf-8')
            print("El cliente nos manda " + Peticion_SIP)
            if not Peticion_SIP:
                break
            (metodo, address, sip) = Peticion_SIP.split()
            if metodo not in ["INVITE", "BYE", "ACK"]:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed" + b"\r\n")
            elif metodo == "INVITE":
                self.wfile.write(b"SIP/2.0 100 Trying" + b"\r\n")
                self.wfile.write(b"SIP/2.0 180 Ring" + b"\r\n")
                self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n")
            elif metodo == "ACK":
                aEjecutar = "mp32rtp -i " + IP + " -p 23032 < " + fichero_audio
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
            elif metodo == "BYE":
                self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request" + b"\r\n")


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    if len(sys.argv) == 4:
        IP = sys.argv[1]
        Port_serv = int(sys.argv[2])
        fichero_audio = sys.argv[3]
        if os.path.exists(fichero_audio):
            serv = socketserver.UDPServer((IP, Port_serv), EchoHandler)
            print("Listening")
            serv.serve_forever()
        else:
            sys.exit("Usage: python server.py IP port audio_file")
    else:
        sys.exit("Usage: python server.py IP port audio_file")
