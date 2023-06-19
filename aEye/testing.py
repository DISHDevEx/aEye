from aEye.video import *

if __name__ == "__main__":
    """
    Main class to run/test video processing framework. Basically
    everything should run as a method for the video object, but theres
    a few limitations: Can't easily multiprocess currently, that's on the horizon for 
    right now, and some methods made with ffmpeg could get ported over to opencv for
    the sake of speed. Video join doesnt work currently. 
    """
    print("--- Video Processing Framework ---")
    video = Video("testVid.mp4") # or any local video, creates Video object
    video.extract_metadata() # Pretty necessary for any video restructuring/processing
    ### Test Video Functions ###
    # All video features come as methods to the Video object, use looks like
    # video.split_on_time(start, end)
    # Example:
    video.split_on_interval(2)  # splits the video into 2 second clips
    video.crop_video_section(400, 400, 500, 200)  # crops a 400x400 section starting at (500,200)
    video.cv_extract_specific_frame(45)  # extracts the 45th frame
    video.cv_extract_frame_at_time(4.655)

