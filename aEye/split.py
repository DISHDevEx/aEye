from video import *
'''
Uses the passed video object (data) to determine at what interval
to split the video, and crops into outputxxx.mp4
Note: Any remainder will just be truncated, so it's likely to end with
a 2 second long final output clip or something, rather than 2 seconds of 
film and 8 of black screen. idk if this is a bad or good thing. 
'''
file = data.getfile()
interval = data.split_interval
cmd = 'ffmpeg -i '+file+' -c copy -v quiet -map 0 -segment_time '+str(interval) + \
      ' -f segment -reset_timestamps 1 output%03d.mp4'
subprocess.call(cmd, shell=True)
