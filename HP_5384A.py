from enum import Enum
import time

class HP_5384A(object):
	def __init__(self, gpib, addr):
		self.address = addr
		self.gpib = gpib
		self.firstTime = True
		self._delay = 0.4
		self.gpib.write("++read_tmo_ms 1200")
		self._preCommand()
	
	class GateTime(Enum):
		T0S1 = 0
		T1S  = 1
		T10S = 2
		
	class Function(Enum):
		FREQ_A = 0
		PER_A  = 1
		FREQ_B = 2
	
	class Digit(Enum):
		INC = 0
		DEC  = 1
		NORMAL = 2
	
	def __str__(self):
		return "HP 5384A address: " + str(self.address)
	
	def _preCommand(self):
		"""Command to be executed before every other command"""
		if self.gpib.address != self.address or self.firstTime:
			self.firstTime = False
			self.gpib.set_address(self.address)
			self.gpib.write("++eor 2")
	
	def get_IDN(self):
		"""Return the ID of the instrument"""
		return self.gpib.get_IDN("ID")
	
	def reset(self):
		"""Reset the instrument to the default state"""
		self._preCommand()
		self.gpib.write("IN")
	
	def enableFilter(self, on):
		"""Enable the filter"""
		self._preCommand()
		if on:
			self.gpib.write("FI1")
		else:
			self.gpib.write("FI0")
			
	def enableAttenuator(self, on):
		"""Enable the attenuator"""
		self._preCommand()
		if on:
			self.gpib.write("AT1")
		else:
			self.gpib.write("AT0")
		
	def setManLevel(self, on):
		"""Set the manual level control"""
		self._preCommand()
		if on:
			self.gpib.write("ML1")
		else:
			self.gpib.write("ML0")
	
	def setGateTime(self, gateTime):
		"""Set the gate time"""
		self._preCommand()
		if gateTime == self.GateTime.T0S1:
			self.gpib.write("GA1")
			self._delay = 0.4
			self.gpib.write("++read_tmo_ms 1200")
		if gateTime == self.GateTime.T1S:
			self._delay = 1.2
			self.gpib.write("GA2")
			self.gpib.write("++read_tmo_ms 1200")
		if gateTime == self.GateTime.T10S:
			self.gpib.write("GA3")
			self._delay = 10.2
			self.gpib.write("++read_tmo_ms 15000")
	
	def measure(self, function):
		"""Take a measurement"""
		self._preCommand()
		if function == self.Function.FREQ_A:
			self.gpib.write("FU1")
		elif function == self.Function.PER_A:
			self.gpib.write("FU2")
		elif function == self.Function.FREQ_B:
			self.gpib.write("FU3")

		try:
			return float(self.gpib.query("++read", sleep=self._delay).replace("F", "").replace("S", "").strip())
		except:
			return False
	
	def digit(self, dig):
		"""Set the digit number"""
		self._preCommand()
		if dig == self.Digit.INC:
			self.gpib.write("DI")
		elif dig == self.Digit.DEC:
			self.gpib.write("DD")
		elif dig == self.Digit.NORMAL:
			self.gpib.write("DN")
	
	def setDisplayState(self, on):
		"""Switch the display on or off"""
		self._preCommand()
		if on:
			self.gpib.write("DL")
		else:
			self.gpib.write("DR            ")
	
	def setDisplayNormal(self):
		"""Set the display to normal mode (Show the measured value)"""
		self._preCommand()
		self.gpib.write("DL")
	
	def setDisplayText(self, text):
		"""Set a custom text on the display (Max 12 character)"""
		self._preCommand()
		self.gpib.write(f"DR{text}")
	
	def local(self):
		"""Go to local mode (Reenable the front panel control)"""
		self._preCommand()
		self.gpib.local()
