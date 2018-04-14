import requests
import hashlib

class API:
    def __init__(self, apikey):
        self.headers = {"apikey": apikey}

    # https://api.metadefender.com/v2/file
    def upload_file(self, filename):
        files = {"filename": open(filename, "rb")}

        url = "https://api.metadefender.com/v2/file"

        r = requests.post(url, headers=self.headers, files=files)

        if r.status_code != 200:
            print("/v2/file/ returned ", r.status_code, file=sys.stderr)
            sys.exit(1)

        res = r.json()

        return res

    # https://api.metadefender.com/v2/file/:dataId
    def file_results(self, data_id):
        url = "https://api.metadefender.com/v2/file/{}".format(data_id)

        r = requests.get(url, headers=self.headers)

        if r.status_code != 200:
            print("/v2/file/ returned ", r.status_code, file=sys.stderr)
            sys.exit(1)

        res = r.json()

        return res

    #hash
    # https://api.metadefender.com/v2/hash/:hash
    def hash_lookup(self, filename):
        h = hashlib.md5()
        with open(filename, "rb", buffering=0) as f:
            for b in iter(lambda: f.read(128 * 1024), b""):
                h.update(b)

        file_md5 = h.hexdigest()

        url = "https://api.metadefender.com/v2/hash/{}".format(file_md5)

        r = requests.get(url, headers=self.headers)

        # a not found hash lookup returns still returns 200
        # i'll assume something's broke if we return something else
        if r.status_code != 200:
            print("/v2/hash/ returned ", r.status_code, file=sys.stderr)
            sys.exit(1)

        res = r.json()

        return res

    def output_results(self, res):
        filename = res["file_info"]["display_name"]
        results = res["scan_results"]["scan_all_result_a"]

        print("filename: {}".format(filename))
        print("overall_status: {}".format(results))
        print("")

        for k, v in res["scan_results"]["scan_details"].items():
            print("engine: {}".format(k))
            print("threat_found: {}".format(v["threat_found"]))
            print("scan_result: {}".format(v["scan_result_i"]))
            print("def_time: {}".format(v["def_time"]))
            print("")