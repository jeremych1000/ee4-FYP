from difflib import SequenceMatcher
from operator import itemgetter


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def print_all_plates(input):
    for pic in input:
        if (len(pic['results']) > 0):
            i = 0
            # pic["results"] is for every pic, whether there are plates detected
            for p in pic['results']:
                i += 1
                print("Plate #%d" % i)
                print("   %12s %12s" % ("Plate", "Confidence"))
                # number of candidates = top_n
                for candidate in p['candidates']:
                    prefix = "-"
                    plate = candidate["plate"]
                    confidence = candidate["confidence"]
                    print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))


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
