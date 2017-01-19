from openalpr import Alpr

def get_plates(input_file_name):
    alpr = Alpr("us", "C:/Users/Jeremy/Documents/GitHub/openalpr/windows/build/dist/2.2.0/v120/Release/x64/openalpr.conf", "C:/Users/Jeremy/Documents/GitHub/openalpr/windows/build/dist/2.2.0/v120/Release/x64/runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(3)
    #alpr.set_default_region("md")

    results = alpr.recognize_file(input_file_name)

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

    # Call when completely done to release memory
    alpr.unload()