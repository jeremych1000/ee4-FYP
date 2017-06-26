import cv2, os, math, shutil, datetime


def split(video_path, video_name, video_ext, wanted_fps=5, verbose=False):
    os.makedirs(video_path + video_name, exist_ok=True)
    if len(os.listdir(video_path + video_name)) > 0:
        print("Folder detected, assuming already split, skipping split. Delete the folder otherwise.")
        return False
    else:
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
        microseconds_per_frame = math.floor(1000000/wanted_fps)

        foo, date, time = video_name.split("_")
        time.replace(".mp4", "")
        datetime_obj = datetime.datetime.strptime(date+time, "%Y%m%d%H%M%S")
        print("Time detected as ", datetime_obj)

        i = 0
        frame = 0
        print("Splitting video into frames", end="", flush=True)
        while i < video_total_frames:
            grab = video_capture.grab()
            frame -= 1

            if frame <= 0 and grab:
                ret, frame = video_capture.retrieve()
                datetime_obj += datetime.timedelta(microseconds=microseconds_per_frame)
                filename_to_write = datetime_obj.strftime("%Y%m%d_%H%M%S_%f")

                cv2.imwrite(video_path + video_name + "/" + str(filename_to_write) + '.png', frame)
                frame = skip_frames_fps
                if verbose: print("Processed frame ", i, " - saved")
            else:
                if verbose: print("Processed frame ", i, " - skipped")

            i += 1
            if (i % 10 == 0):
                print(".", end="", flush=True)

        print("\nDone")
        return True


def del_folder(video_path, video_name):
    full_path = video_path + video_name
    try:
        shutil.rmtree(full_path)
    except Exception as e:
        print("Exception while deleting - ", str(e))
        return False
    return True
