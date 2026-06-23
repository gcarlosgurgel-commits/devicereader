from hardware import device, cpu, memory

device = device.Device()
proc = cpu.CPU()
ram = memory.Memory()

print(device.get_general_information())
print(proc.get_general_information())
print(ram.get_general_information())