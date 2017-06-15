from django.conf import settings
from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.db import *
from django.core.exceptions import *

import requests, datetime, os, itertools, re
from multiprocessing.dummy import Pool

from alpr import models
from alpr.split_video import *
from alpr.get_alpr import *
from alpr.process_results import extract_plates

from client import models as client_models


def natural_sort(l):  # natural sort instead of ASCII sort
    # https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


class Process_Videos(CronJobBase):
    RUN_EVERY_MINS = None
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'alpr.process_videos'

    def do(self):
        main_start = datetime.datetime.now()
        del_folder_on_end = False
        alpr_method = 2  # 1 - serial, 2 - parallel slow, 3 - parallel fast (UNSTABLE! and not really that fast lol)

        try:
            filelist = models.videos.objects.all().filter(processed=False).order_by('filename')
        except ObjectDoesNotExist:
            print("No videos found, terminating.")

        filelist_length = len(filelist)
        if filelist_length == 0:
            print("No videos need to be processed, terminating.")
        else:
            loop_index = 0
            for i in filelist:
                print("\n---\n", loop_index, "/", filelist_length)

                head, tail = os.path.split(i.filename)
                head = head + "/"  # otherwise /home/pi/ee4-FYP/software/peer -  VID_20170528_201314.mp4

                video_name = tail.replace('.mp4', '')
                video_ext = ".mp4"

                print("Begin split")
                ret = split(head, video_name, video_ext, wanted_fps=5, verbose=False)
                print("End split with result - ", ret)

                # get list of images to process
                os_filelist = natural_sort(os.listdir(head + video_name))
                filelist = [head + video_name + "/" + file for file in os_filelist]
                num_files = len(filelist)
                print(num_files, " files detected")

                start = datetime.datetime.now()

                if alpr_method == 1:
                    print("Using serial method")
                    results = []
                    for file in filelist:
                        results.append(get_plates_slow(file))
                        # print(results)
                else:  # parallel
                    pool_size = 3
                    # Make the Pool of workers
                    pool = Pool(pool_size)

                    if alpr_method == 2:
                        print("Using parallel slow method")
                        try:
                            results = pool.map(get_plates_slow, filelist)
                        except Exception as e:
                            print(str(e))
                    elif alpr_method == 3:
                        print("Using parallel fast method")
                        # creatre alpr objects
                        alpr_pool = [create_alpr() for i in range(num_files)]
                        # alpr_pool = [alpr_pool[0]]
                        print(len(alpr_pool), " ALPR objects created")
                        results, dates = pool.starmap(get_plates_fast, zip(alpr_pool, filelist))
                        for i in alpr_pool:
                            i.unload()
                    else:
                        print("Wrong ALPR method specified")

                    # close the pool and wait for the work to finish
                    pool.close()
                    pool.join()

                end = datetime.datetime.now()

                print("\n", len(results), " raw results received from ALPR")
                print("Took ", end - start)
                #print("Results for debug: ", results)
                plates = extract_plates(results)
                print(len(plates), " unique cars detected")
                print("Plates: ", plates)

                for ret_plate, ret_conf, ret_date, ret_filepath in plates:
                    ret_date = timezone.make_aware(ret_date)

                    try:
                        peer_self = client_models.peer_list.objects.get(is_self=True)
                    except ObjectDoesNotExist:
                        print("Peer self does not exist, please register first!")

                    try:
                        client_models.plates.objects.create(
                            timestamp=ret_date,
                            plate=ret_plate,
                            location_lat=peer_self.location_lat,
                            location_long=peer_self.location_long,
                            confidence=ret_conf,
                            source=peer_self,
                            img_path="http://"+str(peer_self.ip_address)+":"+str(peer_self.port)+"/alpr"+str(ret_filepath),
                        )
                    except IntegrityError:
                        print("Integrity Error while adding plate to database.", ret_plate, ret_conf, ret_date)
                    except Exception as e:
                        print("Exception occured - ", str(e))

                # then mark as processed
                i.processed = True
                i.time_processed = timezone.now()
                try:
                    i.save()
                except Exception as e:
                    print("Error while saving - ", str(e))

                # clean up
                if del_folder_on_end:
                    del_folder(head, video_name)

                loop_index += 1

            main_end = datetime.datetime.now()
            print("\n---\nTotal took ", main_end - main_start)
