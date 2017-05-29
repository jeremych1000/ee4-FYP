import cv2, sys
from openalpr import Alpr

def alpr(path):
    alpr = Alpr("eu", "C:\\Users\\Jeremy\\Documents\\GitHub\\openalpr\\windows\\build\\dist\\2.2.0\\v120\\Release\\x64\\openalpr.conf", "C:\\Users\\Jeremy\\Documents\\GitHub\\openalpr\\windows\\build\\dist\\2.2.0\\v120\\Release\\x64\\runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)
        
    alpr.set_top_n(3)
    #alpr.set_default_region("md")

    results = alpr.recognize_file(input)
    #results = alpr.recognize_array(input)

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

    # Call when completely done to release memory
    alpr.unload()

vidcap = cv2.VideoCapture("F:/test_videos/walking/VID_20170528_200924.mp4")

count = 0
success = True
while success:
  success,image = vidcap.read()
  print("Reading ", count, "th frame: ", success)
  name = "frame"+str(count)+".jpg"

  alpr(name)

  cv2.imwrite(name, image)     # save frame as JPEG file
  count += 1