import cv2, os, math, shutil

def split(video_path, video_name, video_ext, wanted_fps=5, verbose=False):
    print("Attempting to open ", video_path + video_name + video_ext)
    try:
        video_capture = cv2.VideoCapture(video_path + video_name + video_ext)
    except Exception as e:
        print("Exception occured - ", str(e))
        return False

    if not video_capture.isOpened():
        print("Video does not exist")
        return False

    video_fps = video_capture.get(cv2.CAP_PROP_FPS)
    video_total_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    skip_frames_fps = math.floor(video_fps / wanted_fps)

    #make video dir if not exist
    os.makedirs(video_path + video_name, exist_ok=True)

    print("Splitting video into frames...", end="")

    i=0
    frame=0
    while i < video_total_frames:
        grab = video_capture.grab()
        frame -= 1

        if frame <= 0 and grab:
            ret, frame = video_capture.retrieve()
            cv2.imwrite(video_path + video_name + "/" + str(i) + '.png', frame)
            frame = skip_frames_fps
            if verbose: print("Processed frame ", i, " - saved")
        else:
            if verbose: print("Processed frame ", i, " - skipped")
        i += 1

    print(" Done")
    return True

def del_folder(video_path, video_name):
    full_path = video_path + video_name
    try:
        shutil.rmtree(full_path)
    except Exception as e:
        print("Exception while deleting - ", str(e))
        return False
    return True
