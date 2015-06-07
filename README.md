# HDHomeWeb
HDHomeRun chromecast/Web streaming, simplified!

This Python script allows you to stream channels from your HDHomeRun to your Chromecast/mobile device (HLS, so iOS and Android). See [here](https://github.com/magmastonealex/HDHomeWeb/wiki/Installing-under-Windows) for how to install under Windows.

It pulls data from HTTP on the HDHomeRun, which provides much, much clearer video amongst heavy network traffic, especially compared to UDP or even RTP mode.

Requires FFmpeg, python2, hdhomerun_config somewhere in $PATH.

To run it:
  - Make sure you've scanned for channels with your HDHomeRun's web interface.
  - `python2 main.py`
  - Visit `http://youriphere:7090/chans.html`
  - Enjoy!

The FFmpeg log file is located at ffmpeg_log.txt.

This script tries to get the name of the network of channels. This works pretty well for American channels, but the CRTC doesn't have a great (well... any) API.


Upcoming features include:

  - ~~Autodetection of HDHomeRuns~~
  - Multiple streams at once (ultrafast h.264 does not take that much CPU).
  - ~~Autodetection of supported codecs (libfdk_aac, while it sounds much better, is not available everywhere)~~
  - ~~Pulling channels from an HDHomeRun.~~
  - ~~Get channel name from CRTC/FCC~~
  
