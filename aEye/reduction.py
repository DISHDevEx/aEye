from video import Video
import logging
import math
from auxiliary import Aux


def set_bitrate(video_list, bitrate):
    """
    Sets the bitrate of the video in KB/s. If bitrate is set as 0, then
    the framework will do a 10x bitrate reduction for the reencode. This usually leaves
    the quality watchable. 

    Parameters
    ----------

    video_list : List[Video]
        List of all the videos loaded currently.

    bitrate.   : Integer
        Desired bitrate for the videos. This is given in Kb, so setting it to 1.5 Mb for exmaple should be 
        1500, not 1.5! Setting to 0 will do a 10x reduction

    Returns
    ----------

    List of videos with the bitrate adjustment label applied. 
    """
    if bitrate == 0:
        tenx = True
    else:
        tenx = False
    for video in video_list:
        try:
            if tenx:
                video.extract_metadata()
                cur_br = int(video.meta_data["streams"][0]["bit_rate"])
                bitrate = math.ceil(cur_br/10000)
            insert_str = f" -x264-params 'nal-hdr=cbr' -b:v {bitrate}K -minrate {bitrate}K -maxrate {bitrate}K -bufsize {(int(bitrate) * 2)}K "
            video.add_label(insert_str)
            video.add_output_title(f"bitrate_{bitrate}K_")
            logging.info(f"Bitrate adjusted. Not perfectly accurately, but thats ok")
        except:
            logging.error(f" Cannot set bitrate to {bitrate}k for video {video}")
    return video_list

def change_fps(video_list, new_framerate):
    """
    Super simple video FPS adjustment. Adjusting FPS up can do some funky things 
    to the video as Mac thinks high framerate videos are slow-mo videos,
    but it still works just fine. 

    Parameters
    ----------

    video_list: List[Video]
        List of all loaded videos 

    new_framerate: Integer
        The desired frame rate for the video to be re-encoded to. Lowering framerate
        will reduce the size of the file drastically, but frames will be lost and it can result in
        a less than ideal viewing experience for humans.

    Returns
    ----------

    List of all videos with the complex filter to change FPS applied
    """
    for video in video_list:
        video.complex_filter.append(f"fps={new_framerate}")
        video.add_output_title(f"framerate_{new_framerate}_")
    return video_list


def main():
    aux=Aux()
    video_list = aux.load_s3(bucket = 'aeye-data-bucket', prefix = 'input_video/')
    change_fps(video_list, 15)
    set_bitrate(video_list, 0)
    out = aux.execute_label_and_write_local(video_list)

    
if __name__ == "__main__":
    main()