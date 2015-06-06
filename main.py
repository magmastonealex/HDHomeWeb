import socket
import sys
import datetime
import time
import os
import SimpleHTTPServer
import subprocess
import SocketServer
from threading import Thread
import time
import signal
import sys
import shutil


os.chdir("tcode")


timer=0
done=False

p=False

def scanTuners():
	p=subprocess.Popen(["hdhomerun_config","discover"],stdout=subprocess.PIPE)
	x=p.communicate()[0]
	return x.split("at")[1].rstrip().replace(" ","")


def ffmpeg_codecs():
	x=subprocess.Popen(["ffmpeg","-codecs"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	y=x.communicate()[0]
	return y.find("libfdk_aac")


channelComp=""
host=""

def start_ffmpeg():
	global channelComp
	global p
	global host
	acodecs=['libfdk_aac', '-ac:a:0', '2', '-vbr', '5']
	if ffmpeg_codecs() == -1:
		print "Hey. You. Get FFmpeg with libfdk_aac! Your ears will thank you!"
		acodecs=["aac","-ac","2","-b:a:0","128k","-strict","-2"]
	logfile = open('/tmp/ffmpeg_log.txt', 'w')
	p=subprocess.Popen(["ffmpeg","-i","http://"+host+":5004/auto/v"+channelComp,"-vcodec","libx264","-preset","veryfast","-acodec"]+acodecs+["-vf","yadif=0:0:0","out.m3u8"],stdout=logfile,stderr=logfile)

def letsgo(chan):
	global done
	global timer
	global p
	global channelComp
	ch=chan.split("_")
#	http://192.168.0.149:5004/auto/v41.1
	channelComp=ch[0]+"."+ch[1]
	thread2 = Thread(target = start_ffmpeg)
	thread2.start()
	while done==False: # get 10MB of the file...
		elapsed_time = time.time() - timer
		print "here "+str(elapsed_time)+" "+str(timer)
		if int(elapsed_time) > 20 and timer != 0:
			done=True
			happening=False
			p.kill()
		time.sleep(5)
	print "over"
	import glob
	files = glob.glob('./*.ts')
	for f in files:
	    os.remove(f)
	os.remove("./out.m3u8")






happening=False
class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def end_headers(self):
		self.send_header("Access-Control-Allow-Origin", "*")
		SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)
	def do_GET(self):
		global done
		global happening
		global timer
		elapsed_time = time.time() - timer
		print elapsed_time
		if timer==0 or elapsed_time < 20:
			timer=time.time()
		else:
			print "Stream finished! Cleaning up!"
			done=True
			happening=False
		if self.path.find("?chan="):
			if happening==False:
				ch=self.path.split("?chan=")
				if len(ch)<2:
					SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
					return
				print ch
				ch=ch[1]
				ch=ch.replace("/","")
				print ch
				try:
					os.remove("./out.m3u8")
				except:
					pass
				th = Thread(target = letsgo, args=(ch,))
				th.start()
				timer=0
				done=False
				happening=True

		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

host=scanTuners()
o=open("ip.txt","w")
o.write(host)
o.close()
#Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

SocketServer.TCPServer.allow_reuse_address=True
httpd = SocketServer.TCPServer(("", 7090), CustomHandler)

httpd.serve_forever()

