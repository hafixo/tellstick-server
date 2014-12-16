 # -*- coding: utf-8 -*-

from Protocol import Protocol
import logging

class ProtocolArctech(Protocol):
	def stringForMethod(self, method):
		if self.model == 'codeswitch':
			return self.stringForCodeSwitch(method)
		logging.warning("Unknown model %s", self.model)

	def stringForCodeSwitch(self, method):
		strHouse = self.stringParameter('house', 'A')
		intHouse = ord(strHouse[0]) - ord('A')
		strReturn = self.codeSwitchTuple(intHouse)
		strReturn = strReturn + self.codeSwitchTuple(self.intParameter('unit', 1, 16)-1)

		if method == 'turnon':
			strReturn = strReturn + '$k$k$kk$$kk$$kk$$k'
		elif method == 'turnoff':
			strReturn = strReturn + '$k$k$kk$$kk$$k$k$k'
		else:
			return None
		return {'S': strReturn}

	def codeSwitchTuple(self, intCode):
		strReturn = ''
		for i in range(4):
			if intCode & 1:  # Convert 1
				strReturn = strReturn + '$kk$'
			else:  # Convert 0
				strReturn = strReturn + '$k$k'
			intCode = intCode >> 1
		return strReturn
