# hp_5384a
Python module for the HP 5384A 225 MHz frequency counter.

You must use my GPIB or GPIB_WIFI module to use this module.

## Supported command:
### get_idn()
Return the ID of the instrument

### reset()
Reset the instrument to the default state

### enable_filter(on)
Set the filter
<table>
  <tr><td>on</td><td>Description</td></tr>
  <tr><td>True</td><td>Enable the filter</td></tr>
  <tr><td>False</td><td>Disable the filter</td></tr>
</table>

### enable_attenuator(on)
Set the attenuator
<table>
  <tr><td>on</td><td>Description</td></tr>
  <tr><td>True</td><td>Enable the attenuator</td></tr>
  <tr><td>False</td><td>Disable the attenuator</td></tr>
</table>

### set_man_level(on)
Set the manual level control
<table>
  <tr><td>on</td><td>Description</td></tr>
  <tr><td>True</td><td>Enable the manual level control</td></tr>
  <tr><td>False</td><td>Disable the manual level control</td></tr>
</table>

### set_gate_time(gate_time)
Set the gate time
<table>
  <tr><td>gateTime</td><td>Description</td></tr>
  <tr><td>HP_5384A.GateTime.T0S1</td><td>Set the gate time to 0.1 seconds</td></tr>
  <tr><td>HP_5384A.GateTime.T1S</td><td>Set the gate time to 1 second</td></tr>
  <tr><td>HP_5384A.GateTime.T10S</td><td>Set the gate time to 10 seconds</td></tr>
</table>

### measure(function)
Take a measurement
<table>
  <tr><td>function</td><td>Description</td></tr>
  <tr><td>HP_5384A.Function.FREQ_A</td><td>Measure frequency on channel A [Hz]</td></tr>
  <tr><td>HP_5384A.Function.PER_A</td><td>Measure period on channel A [Seconds]</td></tr>
  <tr><td>HP_5384A.Function.FREQ_B</td><td>Measure frequency on channel B [Hz]</td></tr>
</table>
Return the measurement as real value

### digit()
Set the digit number
<table>
  <tr><td>gateTime</td><td>Description</td></tr>
  <tr><td>HP_5384A.Digit.INC</td><td>Increment the digit number</td></tr>
  <tr><td>HP_5384A.Digit.DEC</td><td>Decrement the digit number</td></tr>
  <tr><td>HP_5384A.Digit.NORMAL</td><td>Set the default digit number</td></tr>
</table>

### set_display_state(on)
Switch the display on or off
<table>
  <tr><td>on</td><td>Description</td></tr>
  <tr><td>True</td><td>Switch on the display</td></tr>
  <tr><td>False</td><td>Switch off the display</td></tr>
</table>

### set_display_normal()
Set the display to normal mode (Show the measured value) 

### set_display_text(text)
Set a custom `text` on the display (Max 12 character)

### local()
Go to local mode (Reenable the front panel control)

## Usage:
```python
from gpib_all import AR488Wifi
from hp_5384a import HP5384A

gpib = AR488Wifi('192.168.178.36')
freq = HP5384A(gpib, 1)
print(freq)
freq.enable_filter(True)
freq.set_gate_time(HP5384A.GateTime.T1S)
print("freq:", freq.measure(HP5384A.Function.FREQ_A), "Hz")
freq.local()
```
## Result of executing the above code:
```
HP 5384A address: 1
freq: 17200.001 Hz
```
