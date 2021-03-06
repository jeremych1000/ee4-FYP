import sys
from openalpr import Alpr

def get_plates(input, region="eu", top_n=3):
    alpr = Alpr(region, "C:/Users/Jeremy/Documents/GitHub/openalpr/windows/build/dist/2.2.0/v120/Release/x64/openalpr.conf", "C:/Users/Jeremy/Documents/GitHub/openalpr/windows/build/dist/2.2.0/v120/Release/x64/runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(top_n)
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

    #return results