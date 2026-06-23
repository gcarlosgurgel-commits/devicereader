from hardware import device
from hardware import cpu

device = device.Device()
proc = cpu.CPU()

print(device.get_general_information())
print(proc.get_general_information())