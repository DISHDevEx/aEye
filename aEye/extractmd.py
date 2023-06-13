import json
from video import *
'''
Class to extract the metadata of a passed video path 
and kicks the resulting json dictionary back to the main
Video class. 
'''
# Currently need to work on the file path being updated not in here
command  = "ffprobe -hide_banner -show_streams -v error -print_format json -show_format -i '/Users/James.Fagan/Documents/longvid.mp4'"
out = subprocess.check_output(command, shell=True).decode("utf-8")
json_data = json.loads(out)
retval = json_data#["streams"]
print(retval)