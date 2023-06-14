from aEye import Video
from aEye import *


mdCheck = "{'streams': [{'index': 0, 'codec_name': 'h264', 'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part "\
          "10', 'profile': 'Main', 'codec_type': 'video', 'codec_tag_string': 'avc1', 'codec_tag': '0x31637661', " \
          "'width': 1920, 'height': 1080, 'coded_width': 1920, 'coded_height': 1080, 'closed_captions': 0, " \
          "'film_grain': 0, 'has_b_frames': 1, 'pix_fmt': 'yuv420p', 'level': 41, 'color_range': 'tv', 'color_space': "\
          "'bt709', 'color_transfer': 'bt709', 'color_primaries': 'bt709', 'chroma_location': 'left', 'field_order': " \
          "'progressive', 'refs': 1, 'is_avc': 'true', 'nal_length_size': '4', 'id': '0x1', 'r_frame_rate': '25/1', " \
          "'avg_frame_rate': '25/1', 'time_base': '1/25000', 'start_pts': 0, 'start_time': '0.000000', 'duration_ts': "\
          "932000, 'duration': '37.280000', 'bit_rate': '18375447', 'bits_per_raw_sample': '8', 'nb_frames': '932', " \
          "'extradata_size': 40, 'disposition': {'default': 1, 'dub': 0, 'original': 0, 'comment': 0, 'lyrics': 0, " \
          "'karaoke': 0, 'forced': 0, 'hearing_impaired': 0, 'visual_impaired': 0, 'clean_effects': 0, " \
          "'attached_pic': 0, 'timed_thumbnails': 0, 'captions': 0, 'descriptions': 0, 'metadata': 0, 'dependent': 0, "\
          "'still_image': 0}, 'tags': {'creation_time': '2019-11-19T16:35:35.000000Z', 'language': 'eng', " \
          "'handler_name': '\\x1fMainconcept Video Media Handler', 'vendor_id': '[0][0][0][0]', 'encoder': 'AVC " \
          "Coding'}}, {'index': 1, 'codec_name': 'aac', 'codec_long_name': 'AAC (Advanced Audio Coding)', 'profile': " \
          "'LC', 'codec_type': 'audio', 'codec_tag_string': 'mp4a', 'codec_tag': '0x6134706d', 'sample_fmt': 'fltp', " \
          "'sample_rate': '48000', 'channels': 2, 'channel_layout': 'stereo', 'bits_per_sample': 0, " \
          "'initial_padding': 0, 'id': '0x2', 'r_frame_rate': '0/0', 'avg_frame_rate': '0/0', 'time_base': '1/48000', "\
          "'start_pts': 0, 'start_time': '0.000000', 'duration_ts': 1789440, 'duration': '37.280000', 'bit_rate': " \
          "'317375', 'nb_frames': '1750', 'extradata_size': 2, 'disposition': {'default': 1, 'dub': 0, 'original': 0, "\
          "'comment': 0, 'lyrics': 0, 'karaoke': 0, 'forced': 0, 'hearing_impaired': 0, 'visual_impaired': 0, " \
          "'clean_effects': 0, 'attached_pic': 0, 'timed_thumbnails': 0, 'captions': 0, 'descriptions': 0, " \
          "'metadata': 0, 'dependent': 0, 'still_image': 0}, 'tags': {'creation_time': '2019-11-19T16:35:35.000000Z', "\
          "'language': 'eng', 'handler_name': '#Mainconcept MP4 Sound Media Handler', 'vendor_id': '[0][0][0][0]'}}], "\
          "'format': {'filename': '/Users/James.Fagan/Documents/longvid.mp4', 'nb_streams': 2, 'nb_programs': 0, " \
          "'format_name': 'mov,mp4,m4a,3gp,3g2,mj2', 'format_long_name': 'QuickTime / MOV', 'start_time': '0.000000', "\
          "'duration': '37.280000', 'size': '87139287', 'bit_rate': '18699417', 'probe_score': 100, " \
          "'tags': {'major_brand': 'mp42', 'minor_version': '0', 'compatible_brands': 'mp42mp41', 'creation_time': " \
          "'2019-11-19T16:35:35.000000Z'}}}\n"

new_vid_obj = Video("/Users/James.Fagan/Documents/longvid.mp4")
tocheck = extract_metadata(new_vid_obj.getfile())
assert(tocheck == mdCheck)

