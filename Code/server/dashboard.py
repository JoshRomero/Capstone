# This script count the number of times each object has been queried by the user


import matplotlib.pyplot as plt

def dashboard(collection):
    ######## START GET DATA FOR OBJECT QUERIES BY TYPE ############################################################
    # initialize all counts to 0
    remoteQueries = 0
    handbagQueries = 0
    laptopQueries = 0
    cellPhoneQueries = 0
    bookQueries = 0
    
    # search for and count all remote queries
    curObject = "remote"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      remotekQueries += 1
    
    # search for and count all handbag queries
    curObject = "handbag"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      handbagQueries += 1
    
    # search for and count all laptop queries
    curObject = "laptop"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      laptopQueries += 1
    
    # search for and count all cellphone queries
    curObject = "cellphone"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      cellPhoneQueries += 1
    
    # search for and count all book queries
    curObject = "book"
    listQueries = collection.find({ "objectQueried": curObject}, { "objectQueried": 1 } )
    
    for x in listQueries:
      bookQueries += 1
    ######## END GET DATA FOR OBJECT QUERIES BY TYPE ############################################################
    
    
    ######## START GET DATA FOR OBJECT QUERIES BY TIME OF DAY ############################################################
    mornQueries = 0
    aftrQueries = 0
    evenQueries = 0
    
    listQueries = collection.find({"morningQuery": 1}, {"queryDateTime": 1})
    for x in mornQueries:
      mornQueries += 1
    
    listQueries = collection.find({"afterQuery": 1}, {"queryDateTime": 1})
    for x in aftrQueries:
      aftrQueries += 1
    
    listQueries = collection.find({"evenQuery": 1}, {"queryDateTime": 1})
    for x in mornQueries:
      evenQueries += 1
    ######## END GET DATA FOR OBJECT QUERIES BY TIME OF DAY ############################################################
    
    
    # plot results in matplotlib
    
    # first subplot is how many queries by item type
    plt.title("Your Dashboard")
    plt.subplot(2,1,1)
    objNames = ["remote", "handbag", "laptop", "cellphone", "book"]
    numQueries = [remoteQueries, handbagQueries, laptopQueries, cellPhoneQueries, bookQueries]
    plt.bar(objNames, numQueries)
    
    # second subplot is a lines plot how many queries by time of day
    plt.subplot(2,1,2)
    queryTimes = ["morning", "afternoon", "evening"]
    numQueries = [mornQueries, aftrQueries, evenQueries]
    plt.plot(queryTimes, numQueries)
    
    
    # show plot
    plt.show()
    
    # save figure
    plt.savefig("dashboard.jpg")
