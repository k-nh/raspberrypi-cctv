import os
import picamera
import time
import datetime as datetime
count = 0;
camera = picamera.PiCamera()
width = 320
height = 240
def readProperities():
	global width
	global height
	f = open("/home/pi/mobile/hw5/camera.properties", "r")
	b = f.read()
	f.close()
	lines = b.split("\n")
	w = width
	h = height
	for line in lines:
		line = line.strip()
		if(line.find("#")) == 0:
			continue
		if("=" not in line):
			continue
		commands = line.split("=")
		if("width" in commands[0]):
			w = int(commands[1])
		if("height" in commands[0]):
			h = int(commands[1])
	return (w, h)
def takePicture():
	global count
	global camera
	global width
	global height
	(w, h) = readProperities()
	if(w != width or h != height):
		width = w
		height = h
		camera.resolution = (width, height)
	if(count >= 10):
		try:
			fname = "/home/pi/mobile/static/%09d.jpg" % (count-10)
			os.unlink(fname)
		except:
			print("")
	fname = "%09d.jpg" % count
	camera.capture("/home/pi/mobile/static/"+fname, use_video_port=True)
	count += 1
	//사진에 시간 출력
	camera.annotate_background = picamera.Color('black') 
	//출력되는 text 배경 검정색 설정
	camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
	//현재시간 출력 sudo dpkg-reconfigure tzdata 를 이용하여 asia-seoul 한국시간으로 출력
	f = open("/home/pi/mobile/hw5/lastfname.txt", "wt")
	f.write(fname)
	f.close()
	return fname
def stopPicture():
	global camera
	if(camera != None):
		camera.stop_preview()
		camera = None
if(__name__ == "__main__"):
	while(True):
		fname = takePicture()
		print("capture %s, %d, %d" % (fname, width, height))
