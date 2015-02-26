#!/usr/bin/env python
import Adafruit_BBIO.PWM as PWM

import SocketServer
import logging

import ledControl

#Log setting
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

#Global
HOST = ''
PORT = 8888

#Server  handler
class FlashServer(SocketServer.BaseRequestHandler):

	def handle(self):
		while True :
			#Wait for data
			self.data = self.request.recv(1024).strip()
			#Client closed the connexion
			if not self.data :
				break

			#Read the data from socket
			self.data = self.data.decode("UTF-8")

			logging.info("%s send: %s", format(self.client_address[0]), self.data)

			#Remove whitespaces at the end of the string
			self.data.rstrip('\t\r\0\x00')
			#Separate the string in their original form; TCP can combine them
			requestLst = self.data.split("\x00")

			for request in requestLst:
				#Data in string is separated by space
				dataLst = request.split(" ")

				if request.startswith('<policy-file-request/>'):
					#Send flash policy
					logging.info('Sending policy')
					self.request.sendall('<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="' + str(PORT) + '" /></cross-domain-policy>\x00')
				
				elif dataLst[0] == "led" :
					try:
						#Convert string to int
						ms = abs(int(dataLst[1]))
						pin = str(dataLst[2])
						value = abs(int(dataLst[3]))

						if(value > 255) :
							logging.warning('Value is too large! Setting to 255')
							value = 255

					except (ValueError, IndexError) as e:
						#Request is invalid
						logging.error(e[0])
						logging.info('Abandonning request')

					else :
						logging.info('Fading pin %s to value %s in %sms', pin, value, ms)
						ledControl.fadeTo(pin, value, ms)
				
				elif dataLst[0] == "info" :
					if dataLst[1] == "begin" :
						#Do nothing; not yet implemented
						pass
					if dataLst[1] == "close" :
						logging.info('Explicitly closing connexion per client request')
						#Explicitly stop the connexion
						return
					else :
						logging.warning("Unknown request")
						self.request.sendall(("unknown request: " + self.data).encode("UTF-8"))
				
				else :
					#echo
					logging.warning("Unknown request")
					self.request.sendall(("unknown request: " + self.data).encode("UTF-8"))


	def setup(self):
		logging.info("%s connected", format(self.client_address[0]))

	def finish(self):
		logging.info("%s disconnected", format(self.client_address[0]))

try:
	server = SocketServer.TCPServer((HOST, PORT), FlashServer)
	logging.info('Server starting')
	server.serve_forever()

except KeyboardInterrupt:
	pass

finally:
	logging.info('Server stopping')
	server.shutdown()
	PWM.cleanup()
	logging.info('Server stopped')