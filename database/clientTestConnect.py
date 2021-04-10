from pymongo import MongoClient, errors

try:
    mongo_client = MongoClient("mongodb://192.168.1.54:27017")
    print("Connection sucessful")
    try:
        mongo_client.admin.authenticate(name='root', password='40fpciFJ7r&s')
        print("Sucessfully Authenticated")
    except:
        print("Failed Authentication")
        exit(0)
    
    try:
        for db in mongo_client.list_database_names():
            print(db)
    else:
        print("Failed to print databases")
        exit(0)
except:
    print("Connection failed")