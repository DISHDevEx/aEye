from aEye import Video, extract_metadata

"""
trash metadata test class featuring a super epic hardcoded video ref
"""


def test_extract_metadata():
    new_vid_obj = Video("aEye/inputs/testVid.mp4")
    to_check = extract_metadata(new_vid_obj.getfile())
    codec = to_check["streams"][0]["codec_name"]
    assert codec == "h264"
    duration = to_check["streams"][0]["duration"]
    assert duration == "37.280000"
