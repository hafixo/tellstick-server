# -*- coding: utf-8 -*-

from base import Plugin, implements
from board import Board
from tellduslive.base import ITelldusLiveObserver, TelldusLive
from gpio import Gpio
import socket, struct, fcntl

class Led(Plugin):
	implements(ITelldusLiveObserver)


	def __init__(self):
		self.gpio = Gpio(self.context)
		self.live = TelldusLive(self.context)
		self.gpio.initPin('status:red')
		self.gpio.initPin('status:green')
		self.setNetworkLed()

	def liveConnected(self):
		self.setNetworkLed()

	def liveRegistered(self, msg, refreshRequired):
		self.setNetworkLed()

	def liveDisconnected(self):
		self.setNetworkLed()

	def setNetworkLed(self):
		if self.live.isRegistered():
			# We check live status first since we might have connection on another network interface
			self.gpio.setPin('status:red', 0)
			self.gpio.setPin('status:green', 1, brightness=50)
			return
		if self.live.isConnected():
			self.gpio.setPin('status:red', 0)
			self.gpio.setPin('status:green', 1, brightness=50, freq=1)
			return
		if Led.__getIp(Board.networkInterface()) == None:
			self.gpio.setPin('status:red', 1, freq=1)
			self.gpio.setPin('status:green', 0)
			return
		self.gpio.setPin('status:red', 1, brightness=50)
		self.gpio.setPin('status:green', 0)

	@staticmethod
	def __getIp(iface):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sockfd = sock.fileno()
		SIOCGIFADDR = 0x8915
		ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
		try:
			res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
		except:
			return None
		ip = struct.unpack('16sH2x4s8x', res)[2]
		return socket.inet_ntoa(ip)
