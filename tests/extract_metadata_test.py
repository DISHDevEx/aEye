from aEye import Video

"""
trash metadata test class featuring a super epic hardcoded video ref
"""


def test_extract_metadata():
    new_vid_obj = Video("aEye/inputs/testVid.mp4")
    to_check = new_vid_obj.extract_metadata(new_vid_obj.getfile())
    codec = to_check["streams"][0]["codec_name"]
    assert codec == "h264"
    duration = to_check["streams"][0]["duration"]
    assert duration == "37.280000"
