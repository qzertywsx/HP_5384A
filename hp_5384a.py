"""Module providing an interface to the HP 5384A 225 MHz frequency counter"""
from enum import Enum
#import time

class HP5384A():
    """Class to represent the HP 5384A 225 MHz frequency counter"""
    def __init__(self, _gpib, addr):
        self.address = addr
        self.gpib = _gpib
        self.first_time = True
        self.gpib.write("++read_tmo_ms 1200")
        self._pre_command()

    class GateTime(Enum):
        """Enum with the usable gate time"""
        T0S1 = 0
        T1S  = 1
        T10S = 2

    class Function(Enum):
        """Enum with the function of the instrument"""
        FREQ_A = 0
        PER_A  = 1
        FREQ_B = 2

    class Digit(Enum):
        """Enum with the useble digit function"""
        INC = 0
        DEC  = 1
        NORMAL = 2

    def __str__(self):
        return "HP 5384A address: " + str(self.address)

    def _pre_command(self):
        """Command to be executed before every other command"""
        if self.gpib.address != self.address or self.first_time:
            self.first_time = False
            self.gpib.set_address(self.address)
            self.gpib.write("++eor 2")

    def get_idn(self):
        """Return the ID of the instrument"""
        return self.gpib.get_idn("ID")

    def reset(self):
        """Reset the instrument to the default state"""
        self._pre_command()
        self.gpib.write("IN")

    def enable_filter(self, on):
        """Enable the filter"""
        self._pre_command()
        if on:
            self.gpib.write("FI1")
        else:
            self.gpib.write("FI0")

    def enable_attenuator(self, on):
        """Enable the attenuator"""
        self._pre_command()
        if on:
            self.gpib.write("AT1")
        else:
            self.gpib.write("AT0")

    def set_man_level(self, on):
        """Set the manual level control"""
        self._pre_command()
        if on:
            self.gpib.write("ML1")
        else:
            self.gpib.write("ML0")

    def set_gate_time(self, gate_time):
        """Set the gate time"""
        self._pre_command()
        if gate_time == self.GateTime.T0S1:
            self.gpib.write("GA1")
            self.gpib.write("++read_tmo_ms 1200")
        if gate_time == self.GateTime.T1S:
            self.gpib.write("GA2")
            self.gpib.write("++read_tmo_ms 1200")
        if gate_time == self.GateTime.T10S:
            self.gpib.write("GA3")
            self.gpib.write("++read_tmo_ms 15000")

    def measure(self, function):
        """Take a measurement"""
        self._pre_command()
        if function == self.Function.FREQ_A:
            self.gpib.write("FU1")
        elif function == self.Function.PER_A:
            self.gpib.write("FU2")
        elif function == self.Function.FREQ_B:
            self.gpib.write("FU3")

        try:
            self.gpib.write("++read")
            return float(self.gpib.get_string(show_byte=False).\
                replace("F", "").replace("S", "").strip())
        except (ValueError, AttributeError):
            return False

    def digit(self, dig):
        """Set the digit number"""
        self._pre_command()
        if dig == self.Digit.INC:
            self.gpib.write("DI")
        elif dig == self.Digit.DEC:
            self.gpib.write("DD")
        elif dig == self.Digit.NORMAL:
            self.gpib.write("DN")

    def set_display_state(self, on):
        """Switch the display on or off"""
        self._pre_command()
        if on:
            self.gpib.write("DL")
        else:
            self.gpib.write("DR            ")

    def set_display_normal(self):
        """Set the display to normal mode (Show the measured value)"""
        self._pre_command()
        self.gpib.write("DL")

    def set_display_text(self, text):
        """Set a custom text on the display (Max 12 character)"""
        self._pre_command()
        self.gpib.write(f"DR{text}")

    def local(self):
        """Go to local mode (Reenable the front panel control)"""
        self._pre_command()
        self.gpib.local()
