import subprocess
'''
Uses the passed video object (data) to determine at what interval
to split the video, and crops into outputxxx.mp4
Note: Any remainder will just be truncated, so it's likely to end with
a 2 second long final output clip or something, rather than 2 seconds of 
film and 8 of black screen. idk if this is a bad or good thing. 
'''
def split_on_time(interval, file):
      cmd = 'ffmpeg -i '+file+' -c copy -v quiet -map 0 -segment_time '+str(interval) + \
            ' -f segment -reset_timestamps 1 output%03d.mp4'
      subprocess.call(cmd, shell=True)
      #output%03d.mp4 old output naming convention, save 4 l8r
      #-f nut pipe:1 | cat > test     wacky ass pipe output that certainly does something, also save