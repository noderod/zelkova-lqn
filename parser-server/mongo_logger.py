"""
BASICS

Communicates with the Mongo database
"""

import pymongo


client = pymongo.MongoClient(os.environ['URL_BASE'], username=os.environ['MONGO_INITDB_ROOT_USERNAME'],
                            password=os.environ['MONGO_INITDB_ROOT_PASSWORD'])

jobs_db = client["jobs"]
normal_jobs = jobs_db["normal_jobs"]

x = normal_jobs.insert_one(mydict)


# Inserts a document, returns the unique ID of object if succesful
# jobdoc (dict) (dict): Contains all the job information
def new_job(jobdoc):
    try:
        x = normal_jobs.insert_one(mydict)
        return [True, x.inserted_id]
    except:
        return [False, "Could not connect to MongoDB\nContact the system administrator if you see this message"]

