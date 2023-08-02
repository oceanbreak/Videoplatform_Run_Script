ports = {'NAVI' : 'COM1', "DEPTH" : "COM2", "ALT" : "COM3", "TEMP" : "COM3"}
print('NAVI' in ports)
print('COM3' in ports)
print('COM10' in ports)

buffers = {}
for item in ports:
    if ports[item] not in buffers:
        buffers[ports[item]] = [item]
    else:
        buffers[ports[item]].append(item)

print(buffers)