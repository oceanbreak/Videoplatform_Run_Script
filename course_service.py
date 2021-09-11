import sonardatabuffer
import sonarcom
import Course

portBridge = sonardatabuffer.GenerateBuffer('COM13', 9600, 'GPGGA')
portStern = sonardatabuffer.GenerateBuffer('COM14', 9600, 'GPGGA')

for i in range(10):
    bridgeGps = portBridge.getData()
    labGps = portStern.getData()

    course = Course.calculate_course(labGps, bridgeGps)
    vmGps = Course.calculate_vm_coords(labGps, course)

    print(vmGps)