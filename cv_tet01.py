# import cv2
#
# vcap = cv2.VideoCapture("rtsp://admin:admin@192.168.10.86:554/h264")
#
# while(1):
#
#     ret, frame = vcap.read()
#     cv2.imshow('VIDEO', frame)
#     cv2.waitKey(1)


import ffmpeg
stream = ffmpeg.input('rtsp://admin:admin@192.168.10.30:554/h264', ss=0)
#
# stream2 = ffmpeg.filter_(stream1,'drawtext',text="%{pts}",box='1', boxcolor='0x00000000@1', fontcolor='white')
# stream_out = ffmpeg.output(stream, 'output6.mp4')
# ffmpeg.run(stream3)

input = ffmpeg.input('rtsp://admin:admin@192.168.10.30:554/h264')
# audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)

out = ffmpeg.output( input, 'out.mp4')
ffmpeg.view(input)