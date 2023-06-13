from video import *

file = data.getfile()
interval = data.split_interval
cmd = 'ffmpeg -i '+file+' -c copy -v quiet -map 0 -segment_time '+str(interval)+' -f segment -reset_timestamps 1 output%03d.mp4'
subprocess.call(cmd, shell=True)
