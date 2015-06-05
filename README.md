# HDHomeWeb
HDHomeRun chromecast/Web streaming, simplified!

Right now, this script is not capable of too much, just the core functionality. It can start streams from pre-selected channels to chromecasts and web clients (HLS, so Android and iOS).

It pulls data from HTTP on the HDHomeRun, which provides much, much clearer video amongst heavy network traffic, especially compared to UDP or even RTP mode.

Requires FFmpeg (with libfdk_aac for now), python2.

Upcoming features include:

  - ~~Autodetection of HDHomeRuns~~
  - Multiple streams at once (ultrafast h.264 does not take that much CPU).
  - ~~Autodetection of supported codecs (libfdk_aac, while it sounds much better, is not available everywhere)~~
  - ~~Pulling channels from an HDHomeRun.~~
  
