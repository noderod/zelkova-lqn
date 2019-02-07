"""
BASICS

Communicates with the Mongo database
"""

import os
import pymongo



client = pymongo.MongoClient(os.environ['URL_BASE'], port=27017, username=os.environ['MONGO_INITDB_ROOT_USERNAME'],
                            password=os.environ['MONGO_INITDB_ROOT_PASSWORD'])

jobs_db = client["jobs"]
normal_jobs = jobs_db["normal_jobs"]


# Inserts a document, returns the unique ID of object if succesful
# jobdoc (dict) (dict): Contains all the job information
def new_job(jobdoc):
    try:
        x = normal_jobs.insert_one(jobdoc)
        return [True, x.inserted_id]
    except:
        return [False, "Could not connect to MongoDB\nContact the system administrator if you see this message"]



# Returns a list of all user jobs IDs in a JSON format
# {user: username, ids:[]}
def get_all_user_jobs_ids(username):
    cursor = normal_jobs.find({"User":username})
    userdata = {"user":username, "ids":[]}

    for document in cursor:
        userdata["ids"].append(str(document["_id"]))

    return userdata



