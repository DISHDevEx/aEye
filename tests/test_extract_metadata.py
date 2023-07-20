from aEye import Video
from aEye.auxiliary import Aux
import os

"""
basic metadata test to ensure that all the extracted metadata is what it should be.
"""
input_test_video = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data/test_video.mp4')


def test_extract_metadata():
    aux = Aux()
    video_list_2 = aux.load_local(input_test_video)
    print(video_list_2)
    for video in video_list_2:
        x = video.extract_metadata()
        codec = x['streams'][0]['codec_name']
        assert codec == "h264"  # Basic check. Will fail for some more wacky formats (ex DVD's -> MPEG2)