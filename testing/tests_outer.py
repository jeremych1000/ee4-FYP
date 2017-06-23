from tests import do, similar

import json, ast, pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
print("input is ", args.filename)

if args:
    with open(args.filename) as f:
        lines = f.read().splitlines()

    index = 0
    file_list = []
    prewarp_list = []
    exp_result_list = []
    for i in lines:
        if index % 3 == 0:
            # file
            file_list.append(i)
        elif index % 3 == 1:
            # prewarp
            prewarp_list.append(i)
        elif index %3 == 2:
            # results
            exp_result_list.append(ast.literal_eval(i))
        else:
            print("error")
        index += 1

    print("---")
    print(file_list)
    #print(prewarp_list)
    #print(exp_result_list)


    # -------
    fuzzy_thresh = 0.85
    all_ret = []

    all_got = 0
    all_got_f = 0

    all_got_min = 100
    all_got_max = 0

    all_got_f_min = 100
    all_got_f_max = 0

    all_fps = 0
    for i in range(0, len(file_list)):
        pp = pprint.PrettyPrinter(indent=2)

        ret_plates = []
        gotten = []
        missed = []
        extra = []
        ratio = 0

        fgotten = []
        fmissed = []
        fextra = []
        fratio = 0

        ret, fps = do(exact_path=file_list[i], prewarp=prewarp_list[i])
        all_fps += fps
        all_ret.append(ret)

        for r in ret:
            ret_plates.append(r[0])

        # exact
        for p in exp_result_list[i]:
            if p in set(ret_plates):
                gotten.append(p)
            else:
                missed.append(p)
        fextra = list(set(ret_plates)-set(gotten)-set(missed))
        got = round(len(gotten) * 100 / len(exp_result_list[i]), 2)
        all_got += got
        if got < all_got_min:
            all_got_min = got
        if got > all_got_max:
            all_got_max = got
        #fuzzy
        for pl in exp_result_list[i]:
            appended = False
            for plexp in ret_plates:
                if similar(pl, plexp) > fuzzy_thresh:
                    fgotten.append(pl)
                    appended = True
                    break
            if not appended:
                fmissed.append(pl)
        fextra = list(set(ret_plates)-set(fgotten)-set(fmissed))
        fgot = round(len(fgotten) * 100 / len(exp_result_list[i]), 2)
        all_got_f += fgot
        if fgot < all_got_f_min:
            all_got_f_min = fgot
        if fgot > all_got_f_max:
            all_got_f_max = fgot 

        print("From ALPR: ")
        pp.pprint(ret_plates)
        print("From manual extraction: ")
        pp.pprint(exp_result_list[i])

        print("--EXACT MATCH---")
        print("Correct (", len(gotten), "): ", gotten)
        print("Misesd (", len(missed), "): ", missed)
        print("Extra (", len(extra), "): ", extra)
        print("Stats: ", got, "%")

        print("--FUZZY MATCH---")
        print("Correct (", len(fgotten), "): ", fgotten)
        print("Misesd (", len(fmissed), "): ", fmissed)
        print("Extra (", len(fextra), "): ", fextra)
        print("Stats: ", fgot, "%")

    print("\n ------- \n")
    print("Overall Stats")
    print("exact: ", all_got_min, " - ", round(all_got/len(file_list), 2), " - ", all_got_max)
    print("fuzzy: ", all_got_f_min, " - ", round(all_got_f/len(file_list), 2), " - ", all_got_f_max)
    print("fps: ", round(all_fps/len(file_list), 2))
    print("\n ------- \n ------- \n ------- \n ------- \n")
    print("for debug: ")
    pp.pprint(all_ret)