from aEye import Processor

"""
basic metadata test to ensure that all the extracted metadata is what it should be.
"""


def test_extract_metadata():
    process = Processor()
    process.load(bucket='aeye-data-bucket', prefix='input_video/')
    video_list = process.get_video_list()
    for video in video_list:
        to_check = video.extract_metadata()
        codec = to_check["streams"][0]["codec_name"]
        assert codec == "h264"  # Basic basic basic check. Will fail for some more wacky formats (ex DVD's -> MPEG2)
