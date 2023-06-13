import json
import subprocess
'''
Class to extract the metadata of a passed video path 
and kicks the resulting json dictionary back to the main
Video class. 
'''
# Currently need to work on the file path being updated not in here
def extract_metadata(filePath):
    command  = f"ffprobe -hide_banner -show_streams -v error -print_format json -show_format -i '{filePath}'"
    out = subprocess.check_output(command, shell=True).decode("utf-8")
    json_data = json.loads(out)
    return json_data