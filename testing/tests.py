import requests, datetime, os, itertools, re, json, pprint
import cv2, os, math, shutil, datetime
from difflib import SequenceMatcher
from operator import itemgetter

import sys, platform, random, os, datetime
try:
    sys.path.append('/home/jeremych/openalpr/src/bindings/python')
    sys.path.append('/usr/local/lib/python3.5/dist-packages/openalpr')
    from openalpr import Alpr
except IOError:
    print("IOError")

from multiprocessing.dummy import Pool
#from multiprocessing import Pool


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def extract_plates(input, debug=False):
    ret = []
    ret_tmp = []
    date_tmp = None
    similar_threshold = 0.5

    # input is result from ALPR
    empty = True

    for pic, date, filepath in input:
        # print(pic, date, filepath)
        if (len(pic['results']) > 0):
            # pic["results"] is for every pic, whether there are plates detected
            for p in pic['results']:
                # number of candidates = top_n
                for candidate in p['candidates']:
                    plate = candidate["plate"]
                    confidence = candidate["confidence"]
                    # if plate not in ret_tmp, add
                    if len(ret_tmp) == 0:
                        # print("Adding to temp")
                        date_tmp = date
                        ret_tmp = [(plate, confidence, date_tmp, filepath)]
                    else:
                        i_continue = True
                        for (pla, conf, dat, fil) in ret_tmp:
                            if i_continue and similar(pla, plate) < similar_threshold:
                                i_continue = False
                        if i_continue:
                            # same car, continue to append
                            ret_tmp.append((plate, confidence, date_tmp, filepath))
                        else:
                            # new car, start over
                            # get most confident plate and add to ret
                            # https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples
                            sorted_by_confidence = sorted(ret_tmp, key=itemgetter(1),
                                                          reverse=True)  # sort by confidence
                            # print(sorted_by_confidence)
                            ret.append(sorted_by_confidence[0])
                            date_tmp = date
                            ret_tmp = [(plate, confidence, date_tmp, filepath)]  # date as append newest car's time
            empty = False
        else:
            # no plates detected
            empty = empty and True

    if not empty:
        # need to copy the last car into ret, otherwise lost
        sorted_by_confidence = sorted(ret_tmp, key=itemgetter(1), reverse=True)  # sort by confidence
        # print(sorted_by_confidence)
        ret.append(sorted_by_confidence[0])
    else:
        print("No plates detected at all, returning empty list.")
        return []
    # print("rr", ret)
    return ret


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
    microseconds_per_frame = math.floor(1000000/wanted_fps)

    # make video dir if not exist
    os.makedirs(video_path + video_name, exist_ok=True)
    if len(os.listdir(video_path + video_name)) > 0:
        print("Folder detected, assuming already split, skipping split. Delete the folder otherwise.")
        return video_total_frames
    else:
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
        return video_total_frames

def natural_sort(l):  # natural sort instead of ASCII sort
    # https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def get_plates_slow(input):
    region = "gb"
    top_n = 1

    file, prewarp = input
    #print("ALPR: ", prewarp, type(prewarp))

    alpr = Alpr(region, \
                "/home/jeremych/ee4-FYP/testing/openalpr.conf", \
                "/home/jeremych/ee4-FYP/testing/openalpr/runtime_data/")

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(top_n)
    alpr.set_prewarp(prewarp)

    results = alpr.recognize_file(file)
    alpr.unload()

    head, tail = os.path.split(file)
    date = datetime.datetime.strptime(tail, "%Y%m%d_%H%M%S_%f.png")

    print(".", end="", flush=True)
    return results, date, file

def do(videos_path=None, exact_path=None, prewarp=None):
    main_start = datetime.datetime.now()
    del_folder_on_end = False
    alpr_method = 2  # 1 - serial, 2 - parallel slow, 3 - parallel fast (UNSTABLE! and not really that fast lol)

    if exact_path is not None:
        filelist = [exact_path]

    elif videos_path is not None:
        filelist = os.listdir(videos_path)
        filelist = [fname for fname in filelist if fname.endswith('.mp4')]
    else:
        print("Supply somethign at least!")

    filelist_length = len(filelist)
    #print(filelist)
    if filelist_length == 0:
        print("No videos need to be processed, terminating.")
    else:
        loop_index = 0

    for i in filelist:
        print("\n---\n", loop_index, "/", filelist_length)
        print("Processing ", i)
        head, tail = os.path.split(os.path.join(videos_path, i))
        head = head + "/"  # otherwise /home/pi/ee4-FYP/software/peer -  VID_20170528_201314.mp4

        video_name = tail.replace('.mp4', '')
        video_ext = ".mp4"

        print("Begin split")
        ret = split(head, video_name, video_ext, wanted_fps=5, verbose=False)
        print("End split with total no of frames - ", ret)

        # get list of images to process
        os_filelist = natural_sort(os.listdir(head + video_name))
        filelist = [head + video_name + "/" + file for file in os_filelist]
        num_files = len(filelist)
        print(num_files, " images detected")

        start = datetime.datetime.now()

        if alpr_method == 1:
            print("Using serial method")
            results = []
            for z in range(0, len(filelist)):
                results.append(get_plates_slow((filelist[z], prewarp)))
                # print(results)
        else:  # parallel
            pool_size = 3
            # Make the Pool of workers
            pool = Pool(pool_size)

            if alpr_method == 2:
                print("Using parallel slow method")
                prewarp_list = [prewarp] * len(filelist)
                # print(len(prewarp_list), len(filelist))
                # print(filelist, prewarp_list)
                try:
                    results = pool.map(get_plates_slow, zip(filelist, prewarp_list))
                except Exception as e:
                    print(str(e))
            else:
                print("Wrong ALPR method specified")

            # close the pool and wait for the work to finish
            pool.close()
            pool.join()

        end = datetime.datetime.now()

        print("\n", len(results), " raw results received from ALPR")
        print("Took ", end - start)
        fps = round((num_files / (end-start).total_seconds()), 2)
        print("FPS: ", fps)
        #print("Results for debug: ", results)
        plates = extract_plates(results)
        print(len(plates), " unique cars detected")

        #pp = pprint.PrettyPrinter(indent=2)
        #print("Plates: ")
        #pp.pprint(plates)


        loop_index += 1

    main_end = datetime.datetime.now()
    print("\n---\nTotal took ", main_end - main_start)
    return plates, fps

#do("/mnt/hgfs/test_videos/highstken")
#get_plates_slow("/mnt/hgfs/test_videos/highstken/VID_20170619_161013/20170619_161013_200000.png")
