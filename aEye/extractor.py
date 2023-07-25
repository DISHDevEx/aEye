import cv2
import logging
import os
import tempfile
from aEye.auxiliary import Aux

class Extractor:
    """
    The Extractor class is used for frame extractions using openCV. Any time the methods
    within the Extractor are run, they will instantly execute. To get frames from processed
    videos, use Aux.execute_label_and_write_local and pass the resulting list to the extractor.

    Methods
    --------

    frame_at_time_extractor(aux, video_list, time) -> List[Video]
        Given a time as a float, extract the frame at that point and put it in the temp output folder

    specific_frame_extractor(aux, video_list, frame) -> List[Video]
        Will extract the frame # that is passed in and store it as a PNG in the temp folder

    multiple_frame_extractor(aux, video_list, start_frame, num_frames) -> List[Video]
        Extract the next num_frames after start_frame and send ALL the images to the output folder. This has the
        capacity to create a HUGE amount of images per video, use with caution!

    Examples
    --------

    frame_at_time_extractor(aux, s3_videos, 10) -> Output images come from timestamp 10s

    specific_frame_extractor(aux, s3_videos, 320) -> Output image comes from frame 320

    multiple_frame_extractor(aux, s3_videos, 634, 10) -> Extract 10 contiguous frames starting from 634
    """

    def frame_at_time_extractor(self, aux, video_list, time):
        """
        Given a time in seconds, this will extract the closest frame.
        Img extraction that takes less than half as long as the FFMpeg version.

        Parameters
        -------
        aux         : Auxiliary Loader
            Sets the output path and creates tmp folder

        video_list : List[Video]
            List of all video objects loaded for processing.

        time       : Float
            Time in seconds to extract frame. Can be a float for higher degree of specificity

        Returns
        -------

        Returns a list of videos, but creates an image in the output folder
        """
        for video in video_list:
            try:
                assert float(video.get_duration()) >= time >= 0
                if video.label != '':
                    logging.error(
                        f"WARNING: Video {video} has processing to execute still! Resulting images will NOT have these modifications applied!")
                if video.out != '':
                    file_path = video.out.strip("'")
                else:
                    file_path = video.get_presigned_url().strip("'")
                cv_video = cv2.VideoCapture(file_path)
                fps = cv_video.get(cv2.CAP_PROP_FPS)
                frame_id = int(fps * time)
                cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
                ret, frame = cv_video.read()
                actual_title = os.path.splitext(video.title)[0]
                if video.path is None:
                    video.path = tempfile.mkdtemp(dir="")
                    path = video.path
                    aux._local_path = path
                    aux._temp_folder = path
                else:
                    path = file_path.split('/')[0]
                # if video.path is None:
                #     path = file_path.split('/')[0]
                # else:
                #     path = video.path
                cv2.imwrite(f"{path}/output_cv_extract_frame_at_time_{time}_{actual_title}.png", frame)
                cv_video.release()
                logging.info(f"Extracted frame at time {time}")
            except:
                logging.error(f" Cannot extract frame at time {time} for video {video}")
        return video_list

    def specific_frame_extractor(self, aux, video_list, frame):
        """
        OpenCv method to grab a single frame as a PNG. Passed argument frame is the frame that
        will be extracted. (No decimals please)

        Parameters
        -------

        aux         : Auxiliary Loader
            Sets the output path and creates tmp folder

        video_list : List[Video]
            List of all video objects loaded for processing.

        frame      : Integer
            The frame number to be saved as a PNG

        Returns
        -------

        Returns a list of video objects and outputs an image.
        """
        for video in video_list:
            try:
                assert int(video.get_num_frames()) >= frame >= 0
                if video.label != '':
                    logging.error(
                        f"WARNING: Video {video} has processing to execute still! Resulting images will NOT have these modifications applied!")
                if video.out == '':
                    file_path = video.get_presigned_url().strip("'")
                else:
                    file_path = video.out.strip("'")
                cv_video = cv2.VideoCapture(file_path)
                cv_video.set(cv2.CAP_PROP_POS_FRAMES, frame)
                ret, output = cv_video.read()
                actual_title = os.path.splitext(video.title)[0]
                if video.path is None:
                    video.path = tempfile.mkdtemp(dir="")
                    path = video.path
                    aux._local_path = path
                    aux._temp_folder = path
                else:
                    path = file_path.split('/')[0]
                # if video.path is None:
                #     path = file_path.split('/')[0]
                # else:
                #     path = video.path
                cv2.imwrite(f"{path}/output_cv_extract_specific_frame_{frame}_{actual_title}.png", output)
                logging.info(f"Frame #{frame} extracted ")
                cv_video.release()
            except:
                logging.error(f" Cannot extract frame {frame} for video {video}")
        return video_list

    def multiple_frame_extractor(self, aux, video_list, start_frame, num_frames):
        """
        Given a start_frame, extract the next num_frames from the video, and store the resulting
        collection of frames in the output folder. num_Frames is the number of frames to be returned
        Has the potential to create like a million images, only use this when you REALLY need a lot
        of frames or a specific set of frames.

        Parameters
        -------

        aux         : Auxiliary Loader
            Sets the output path and creates tmp folder

        video_list  : List[Video]
            List of all video objects loaded for processing.

        start_frame : Integer
            Number of the frame at which to start all the frame grabs.

        num_frames  : Integer
            Number of frames to extract. THIS IS THE AMOUNT OF IMAGES PER VIDEO YOU WANT.
            UNLESS YOU NEED A TON OF CONTIGUOUS FRAMES, DO NOT SET THIS TO A HIGH NUMBER.

        Returns
        -------

        Returns a list of Videos, and many frames are output as PNG's
        """
        for video in video_list:
            try:
                if video.label != '':
                    logging.error(
                        f"WARNING: Video {video} has processing to execute still! Resulting images will NOT have these modifications applied!")
                if video.out == '':
                    file_path = video.get_presigned_url().strip("'")
                else:
                    file_path = video.out.strip("'")
                vid_obj = cv2.VideoCapture(file_path)
                actual_title = os.path.splitext(video.title)[0]
                if video.path is None:
                    video.path = tempfile.mkdtemp(dir="")
                    path = video.path
                    aux._local_path = path
                    aux._temp_folder = path
                else:
                    path = file_path.split('/')[0]
                # if video.path is None:
                #     path = file_path.split('/')[0]
                # else:
                #     path = video.path
                #  Sets the relative file location
                for x in range(num_frames):
                    vid_obj.set(cv2.CAP_PROP_POS_FRAMES, start_frame + x)
                    ret, frame = vid_obj.read()
                    fn = f"{path}/output_extract_many_frames_{start_frame}_{num_frames}_{actual_title}_{x}.png"
                    #fn = f"images/output_extract_many_frames_{start_frame}_{num_frames}_{actual_title}_{x}.png"
                    cv2.imwrite(fn, frame)
                vid_obj.release()
                logging.info(f"Extracted {num_frames} from video, saved as PNG's")
            except:
                logging.error(f" Cannot extract {num_frames} starting from frame {start_frame}!")
        return video_list
