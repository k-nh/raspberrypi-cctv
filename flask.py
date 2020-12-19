import sys
sys.path.append("..")

import ch07.jmlee_gpio as jmlee_gpio
import ch07.jmlee_ias jmlee_i2c
import ch08.lab6Spi as lab6Spi
import hw5.camera as camera
import importlib
import time
import ch07.imagescan as imagescan
from flask import Flask, render_template, request
app = Flask(__name__, template_folder = '../templates', static_url_path='/', static_folder='../static')


@app.route("/")
def hello():
	return "hello world"

@app.route("/jmlee")
def jmleeUnderRoot():
	return "<h1>This is under /jmlee</h1>"

@app.route("/templateHtml")
def templateHtml():
	return render_template("index.html")

@app.route("/gpio/<name>", methods=['GET', 'POST'])
def controlGpio(name):
	global jmlee_gpio

	jmlee_gpio = importlib.reload(jmlee_gpio)
	if(name == 'led'):
		return jmlee_gpio.controlled(request.args.get("ison"))
	if(name=='switch'):
		return jmlee_gpio.getSwitch()

	return "Under construction"

@app.route("/i2c")
def controli2cWithTemplate():
	global jmlee_i2c
	temp = jmlee_i2c.getTemperature()
	humi = jmlee_i2c.getHumidity()
	return render_template("i2c.html", path=request.path, temperature=temp, humidity=humi)

@app.route("/camera/<command>")
def controlCamera(command):
	if(command == 'start'):
		fname = camera.takePicture()
	else:
		jmlee_camera.stopPicture()
	return render_template("camera.html", path = request.path, fname = fname)

@app.route("/camera/cctv")
def resizeCamera():
	lastfile = open("/home/pi/mobile/hw5/lastfname.txt", 'r')
	lastname = lastfile.readline()
	fname2 = "/home/pi/mobile/static/"+lastname
	fname = camera.takePicture()
	fname3 = "/home/pi/mobile/static/"+fname
	value = imagescan.scan(fnamefname3)
	// 저장된 가장 마지막사진과 현재 찍은 사진을 비교해서 오차율을 구함
	print(value)
	if(value > 10):
		jmlee_gpio.controlled('ON')
		message = "움직임 감지" //html 에서 나오는 메세지
	else:
		jmlee_gpio.controlled('OFF')
		message = "이상없음" //html 에서 나오는 메세지
	return render_template("camera.html", path = request.path, fname = fname, message = message)

@app.route("/spi")
def printIlluminance():
	global lab6Spi
	illu = lab6Spi.getIlluminance()
	if (illu>2000):
		jmlee_gpio.controlled('ON')
	else:
		jmlee_gpio.controlled('OFF')
	return render_template("spi.html", path=request.path, illuminance = illu)

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8094)
