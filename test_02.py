from lib.folder_struct.Settings import Settings

settings = Settings()
settings.readSettings()
print(settings)
settings.writeSettings()


ports = {'NAVI' : 'COM1', "DEPTH" : "COM2", "ALT" : "COM3", "TEMP" : "COM3"}
ports = {settings.navi_port : settings.navi_port.port,
         settings.depth_port : settings.depth_port.port,
         settings.altimeter_port : settings.altimeter_port.port,
         settings.temp_port : settings.temp_port.port,
         settings.inclin_port : settings.inclin_port.port}


buffers_settings_list = {}
for item in ports:
    if ports[item] not in buffers_settings_list:
        if item.enable:
            buffers_settings_list[ports[item]] = (item.rate, [item.message])
    else:
        if item.enable:
            buffers_settings_list[ports[item]][-1].append(item.message)

print(buffers_settings_list)