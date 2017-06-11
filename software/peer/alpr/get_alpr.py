import sys, platform, random, os, datetime
try:
    sys.path.append('/home/pi/openalpr/src/bindings/python')
    from openalpr import Alpr
except ImportError:
    print("Trying openalpr import")

def create_alpr(region="gb", top_n=1):
    if platform.system().lower().find("windows") != -1:
        # print("Windows")
        alpr = Alpr(region,
                    "C:/Users/Jeremy/Documents/GitHub/openalpr/windows/build/dist/2.2.0/v120/Release/x64/openalpr.conf",
                    "C:/Users/Jeremy/Documents/GitHub/openalpr/windows/build/dist/2.2.0/v120/Release/x64/runtime_data")
    else:  # raspian
        # print("Not Windows")
        alpr = Alpr(region, "/usr/share/openalpr/config/openalpr.defaults.conf", "/usr/share/openalpr/runtime_data/")

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(top_n)
    return alpr

def unload_alpr(alpr_obj):
    alpr_obj.unload()

def get_plates_fast(alpr, input="/dev/shm/mjpeg/cam.jpg"):
    results = alpr.recognize_file(input) #TODO this is so stupid

    debug = False
    if debug:
        print("results is ", results, " with length ", len(results['results']))
        if (len(results['results']) > 0):
            i = 0
            for plate in results['results']:
                i += 1
                print("Plate #%d" % i)
                print("   %12s %12s" % ("Plate", "Confidence"))
                for candidate in plate['candidates']:
                    prefix = "-"
                    if candidate['matches_template']:
                        prefix = "*"

                    print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
        else:
            print("No plates found.")
    else:
        return results

def get_plates_slow(input):
    region = "gb"
    top_n = 1

    if platform.system().lower().find("windows") != -1:
        # print("Windows")
        alpr = Alpr(region,
                    "C:/Users/Jeremy/Documents/GitHub/openalpr/windows/build/dist/2.2.0/v120/Release/x64/openalpr.conf",
                    "C:/Users/Jeremy/Documents/GitHub/openalpr/windows/build/dist/2.2.0/v120/Release/x64/runtime_data")
    else:  # raspian
        # print("Not Windows")
        alpr = Alpr(region, "/home/pi/ee4-FYP/software/peer/alpr/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data/")

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(top_n)
    results = alpr.recognize_file(input)
    alpr.unload()

    head, tail = os.path.split(input)
    date = datetime.datetime.strptime(tail, "%Y%m%d_%H%M%S_%f.png")

    print(".", end="", flush=True)
    return results, date, input