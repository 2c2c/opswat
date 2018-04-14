import sys
import time

import API

# change this
API_KEY = ""


def run(filename):
    api = API.API(API_KEY)
    
    hash_res = api.hash_lookup(filename)
    if "file_id" in hash_res.keys():
        api.output_results(hash_res)
        return

    file_res = api.upload_file(filename)
    data_id = file_res["data_id"]

    res = {}
    # if scan_results is in the object response, we're in queue
    # continue requesting the results until this changes
    while "scan_results" not in res.keys():
        res = api.file_results(data_id)
        time.sleep(1)

    # continue requesting until progress_percentage is 100%
    while res["scan_results"]["progress_percentage"] != 100:
        res = api.file_results(data_id)
        time.sleep(1)

    api.output_results(res)


if len(sys.argv) != 2:
    print("Usage: python upload_file.py filename")
    sys.exit(1)

run(sys.argv[1])