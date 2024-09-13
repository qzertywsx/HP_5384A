from enum import Enum

class HP_5384A(object):
	def __init__(self, gpib, addr):
		self.address = addr
		self.gpib = gpib
		self.firstTime = True
		self.gpib.write("++read_tmo_ms 1200")
		self.preCommand()
	
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
	
	def preCommand(self):
		if self.gpib.address != self.address or self.firstTime:
			self.firstTime = False
			self.gpib.set_address(self.address)
			self.gpib.write("++eor 2")
	
	def get_IDN(self):
		return self.gpib.get_IDN("ID")
	
	def reset(self):
		self.preCommand()
		self.gpib.write("IN")
	
	def setFilter(self, on):
		self.preCommand()
		if on:
			self.gpib.write("FI1")
		else:
			self.gpib.write("FI0")
			
	def setAttenuator(self, on):
		self.preCommand()
		if on:
			self.gpib.write("AT1")
		else:
			self.gpib.write("AT0")
		
	def setManLevel(self, on):
		self.preCommand()
		if on:
			self.gpib.write("ML1")
		else:
			self.gpib.write("ML0")
	
	def setGateTime(self, gateTime):
		self.preCommand()
		if gateTime == self.GateTime.T0S1:
			self.gpib.write("GA1")
			self.gpib.write("++read_tmo_ms 1200")
		if gateTime == self.GateTime.T1S:
			self.gpib.write("GA2")
			self.gpib.write("++read_tmo_ms 1200")
		if gateTime == self.GateTime.T10S:
			self.gpib.write("GA3")
			self.gpib.write("++read_tmo_ms 15000")
	
	def measure(self, function):
		self.preCommand()
		if function == self.Function.FREQ_A:
			self.gpib.write("FU1")
		elif function == self.Function.PER_A:
			self.gpib.write("FU2")
		elif function == self.Function.FREQ_B:
			self.gpib.write("FU3")
		
		try:
			return self.gpib.query("++read")
			return float(self.gpib.query("++read").replace("F", "").replace("S", "").strip())
		except:
			return False
	
	def setDisplay(self, on):
		self.preCommand()
		if on:
			self.gpib.write("DL")
		else:
			self.gpib.write("DR            ")
	
	def setDisplayNormal(self):
		self.preCommand()
		self.gpib.write("DL")
	
	def setDisplayText(self, text):
		self.preCommand()
		self.gpib.write(f"DR{text}")
	
	def digit(self, dig):
		self.preCommand()
		if dig == self.Digit.INC:
			self.gpib.write("DI")
		elif dig == self.Digit.DEC:
			self.gpib.write("DD")
		elif dig == self.Digit.NORMAL:
			self.gpib.write("DN")
	
	def local(self):
		self.preCommand()
		self.gpib.local()
