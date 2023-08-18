################################################
###                                          ###
###  SONARLAB's OceanRecord software         ###
###  for communication with TUV Videomodule  ###
###  designed in Sonarlab                    ###
###  Shirshov Institute of Oceanology        ###
###  Russian Academy of Science              ###
###                                          ###
################################################

from lib.MainApplication import MainApplication

if __name__ == '__main__':
   
    app = MainApplication()

    try:

        app.mainUI.mainloop()

    except BaseException as e:
        
        print(e)
        app.buffers.stopWritingBuffers()