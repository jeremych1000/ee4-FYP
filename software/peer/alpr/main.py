import requests, datetime, os, itertools, re
from multiprocessing.dummy import Pool

from .split_video import *
from .get_alpr import *
from .process_results import extract_plates


def natural_sort(l):  # natural sort instead of ASCII sort
    # https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


video_path = "F:/test_videos/walking/"
os_videolist = [f for f in os.listdir(video_path) if os.path.isfile(os.path.join(video_path, f))]
print("Video list: ", os_videolist)

main_start = datetime.datetime.now()
del_folder_on_end = False
alpr_method = 1  # 1 - serial, 2 - parallel slow, 3 - parallel fast

# os_videolist = ['VID_20170528_201314.mp4']
for i in os_videolist:
    print("\n---\n")

    video_name = i.replace('.mp4', '')
    video_ext = ".mp4"

    ret = split(video_path, video_name, video_ext, wanted_fps=5, verbose=False)

    # get list of images to process
    os_filelist = natural_sort(os.listdir(video_path + video_name))
    filelist = [video_path + video_name + "/" + file for file in os_filelist]
    num_files = len(filelist)
    print(num_files, " files detected")

    start = datetime.datetime.now()

    if alpr_method == 1:
        results = []
        for file in filelist:
            results.append(get_plates_slow(file))
    else:  # parallel
        pool_size = 4
        # Make the Pool of workers
        pool = Pool(pool_size)

        if alpr_method == 2:
            print("Using slow method")
            try:
                results = pool.map(get_plates_slow, filelist)
            except Exception as e:
                print(str(e))
        elif alpr_method == 3:
            # creatre alpr objects
            alpr_pool = [create_alpr() for i in range(num_files)]
            # alpr_pool = [alpr_pool[0]]
            print(len(alpr_pool), " ALPR objects created")
            results = pool.starmap(get_plates_fast, zip(alpr_pool, filelist))
            for i in alpr_pool:
                i.unload()
        else:
            print("Wrong ALPR method specified")

        # close the pool and wait for the work to finish
        pool.close()
        pool.join()

    end = datetime.datetime.now()

    print(len(results), " results received from ALPR")
    print("Took ", end - start)
    # print("Results for debug: ", results)
    plates = extract_plates(results)
    print("Plates: ", plates)
    if del_folder_on_end:
        del_folder(video_path, video_name)

main_end = datetime.datetime.now()
print("\n---\nTotal ", len(i), " videos took ", main_end - main_start)
