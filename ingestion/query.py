import json
import requests
import time
import os
import sys
from calendar import monthrange

# Make sure you replace `username`, `password`, `your-instance`, and `port`
# with the values for your deployment.
url = "http://localhost:8888/druid/v2/sql/task/"


day = sys.argv[1]
month = int(sys.argv[2])
year = int(sys.argv[3])
owner_code = sys.argv[4]
app = sys.argv[5]
maxNumTask = int(sys.argv[6])

# Total of task at the same time
capacity = (requests.request("GET",
                             "http://localhost:8888/druid/indexer/v1/workers",
                             headers={},
                             data={}).json())[0]["worker"]["capacity"]

with open("queries.json") as archive:
    queries = json.load(archive)


def query_type(name):
    if "clicks" in name:
        return "CLICK PRODUCT"
    elif "eventprods" in name:
        if "ADD_TO_CART" in name:
            return "EVENT PRODS ADD TO CART"
        elif "CONVERSION" in name:
            return "EVENT PRODS CONVERSION"
        elif "VIEW_PRODUCT" in name:
            return "EVENT PRODS VIEW PRODUCT"
    elif "ABOUT" in name:
        return "EVENT ABOUT"
    elif "ADD_TO_CART" in name:
        return "EVENT ADD TO CART"
    elif "CONVERSION" in name:
        return "EVENT CONVERSION"
    elif "TEST" in name:
        return "EVENT TEST"
    elif "VIEW_PRODUCT" in name:
        return "EVENT VIEW PRODUCT"
    elif "products" in name:
        return "PRODUCTS"
    elif "EMPTY" in name:
        return "SEARCH EMPTY"
    elif "IMAGE" in name:
        return "SEARCH IMAGE"
    elif "SKETCH" in name:
        return "SEARCH SKETCH"
    elif "TEXT" in name:
        return "SEARCH TEXT"
    elif "stats" in name:
        return "STATS"
    elif "visitors" in name:
        return "VISITORS"
    else:
        return "UNKNOWN"


def query_selector(fileType, queries):
    if fileType == "CLICK PRODUCT":
        return queries[fileType]
    if fileType == "EVENT ABOUT":
        return queries["EVENT"]
    if fileType == "EVENT ADD TO CART":
        return queries["EVENT"]
    if fileType == "EVENT CONVERSION":
        return queries["EVENT"]
    if fileType == "EVENT TEST":
        return queries["EVENT"]
    if fileType == "EVENT VIEW PRODUCT":
        return queries["EVENT"]
    if fileType == "PRODUCTS":
        return queries[fileType]
    if fileType == "SEARCH EMPTY":
        return queries["SEARCH TEXT"]
    if fileType == "SEARCH IMAGE":
        return queries[fileType]
    if fileType == "SEARCH SKETCH":
        return queries[fileType]
    if fileType == "SEARCH TEXT":
        return queries["SEARCH TEXT"]
    if fileType == "VISITORS":
        return queries[fileType]
    if fileType == "EVENT PRODS ADD TO CART":
        return queries["EVENT PRODS"]
    if fileType == "EVENT PRODS CONVERSION":
        return queries["EVENT PRODS"]
    if fileType == "EVENT PRODS VIEW PRODUCT":
        return queries["EVENT PRODS"]
    else:
        return ""


def create_path(directory, month, year, code, day, app):
    return (directory + '/' + code + "/export_day." + app + "." +
            str(year) + str(month).zfill(2) +
            str(day).zfill(2) + ".all_json")


days = monthrange(year, month)[1]

# List of JSON FILES that it's not necesary to be uploaded
not_upload = ["EVENT PRODS ADD TO CART", "EVENT PRODS VIEW PRODUCT",
              "EVENT VIEW PRODUCT", "EVENT ADD TO CART", "EVENT ABOUT",
              "CLICK PRODUCT", "STATS", "UNKNOWN", "EVENT TEST"]

# The following code, allows to ingest a whole month to
# Apache Druid

directory = "/media/data-disk/data/"
path = create_path(directory, month, year, owner_code, day, app)
# Format '2010-01-01T00:00:00Z'
date = str(year) + "-" + str(month) + "-" + str(day) + "T00:00:00Z"
with os.scandir(path) as files:
    files = [file.name for file in files if file.is_file()
             and file.name.endswith('.json')]
    for file in files:
        fileType = query_type(file)
        if fileType not in not_upload:
            if fileType == "PRODUCTS" or fileType == "VISITORS":
                query = (query_selector(fileType, queries) %
                         (owner_code, fileType, path, file, date))
            else:
                query = (query_selector(fileType, queries) %
                         (owner_code, fileType, path, file))

            payload = json.dumps({
                "query": query,
                "context": {
                    "maxNumTasks": maxNumTask
                            }
                                    })
            headers = {
                'Content-Type': 'application/json'
            }
            while ((capacity -
                    len(requests.request("GET", "http://localhost:8888/\
                                                druid/indexer/v1/\
                                                runningTasks",
                                         headers={},
                                         data={}).json())) <= maxNumTask):
                pass
            response = requests.request("POST", url, headers=headers,
                                        data=payload)
            time.sleep(2)
            if (fileType == "SEARCH TEXT" or fileType == "SEARCH SKETCH" or
                    fileType == "SEARCH IMAGE" or fileType == "SEARCH EMPTY"):
                while ((capacity -
                        len(requests.request("GET", "http://localhost:8888/\
                                                    druid/indexer/v1/\
                                                    runningTasks",
                                             headers={},
                                             data={}).json())) <=
                        maxNumTask):
                    pass
                query = (query_selector(fileType, queries) %
                         (owner_code, "SEARCH", path, file))
                payload = json.dumps({
                                        "query": query,
                                        "context": {
                                            "maxNumTasks": maxNumTask
                                                    }
                                        })
                response = requests.request("POST", url, headers=headers,
                                            data=payload)
                time.sleep(2)
