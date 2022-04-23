import pymongo


def retrieve_client():
    # username = 'shivam'
    # password = 'see in mongo database'
    # cluster = 'mycustomcluster.uhyrf.mongodb.net'
    # authSource = 'dbAdmin'
    # authMechanism = 'SCRAM-SHA-1'
    uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + '/?authSource=' + authSource + '&authMechanism='+authMechanism  +'&retryWrites=true&w=majority'
    client = pymongo.MongoClient(uri)
    result = client["mytestdb"]["collection1"].find()
    print("DB CONNECTED")
    return client
