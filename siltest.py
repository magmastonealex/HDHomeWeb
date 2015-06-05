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

def sendMessage(socke,mess):
	tsend=str(len(mess)).ljust(8)+mess
	socke.send(tsend.encode("utf-8"))
	if(mess != "DONE"):
		mlen=int(socke.recv(8).decode("utf-8"))
		return socke.recv(mlen).split("[]:[]")

def handshake(socky):
	st="MYTH_PROTO_VERSION 77 WindMark"
	resp=sendMessage(socky,st)
	if resp[0]=="ACCEPT":
		print "good"
	else:
		print "bad!"
		sys.exit()
timer=0
done=False


p=False
channelComp=""

def start_ffmpeg():
	global channelComp
	global p
	p=subprocess.Popen(["ffmpeg","-i","http://192.168.0.149:5004/auto/v"+channelComp,"-vcodec","libx264","-preset","ultrafast","-acodec","aac","-ac","2","-b:a:0","128k","-strict","-2","-vf","yadif=0:0:0","out.m3u8"])

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
		if elapsed_time > 20 and timer != 0:
			done=True
			happening=False
			p.kill()
		time.sleep(5)
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
			print "WEDONEHERE"
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

#Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
SocketServer.TCPServer.allow_reuse_address=True
httpd = SocketServer.TCPServer(("", 7090), CustomHandler)
#.allow_reuse_address=True

httpd.serve_forever()
