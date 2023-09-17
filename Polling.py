#This program takes a csv file of polling information in the following column format:
#Province, Electoral District Name, Electoral District Number, Population, Electors,
#Polling Stations, Valid Ballots, Percentage of Valid Ballots,Rejected Ballots,
#Percentage of Rejected Ballots, Total Ballots Cast, Percentage of Voter Turnout.
#It performs many functions:
#it displays the polling stations, number of valid ballots, total ballots cast, and
#percentage of voter turnout based on a district number, the electoral districts given a province,
#finds the minimum and maximum value of a given item, displays the total ballots cast from each of the 13 provinces,
#and is able to do insertion sort on data and a binary search on voter percentage given a district number


"""
This function reads the data from the csv file and creates a list of dictionaries.
Parameter is the text file name, returns the list of dictionaries.
"""
def readData(textFile):
    f = open(textFile, "r")
    fileLists = f.readlines()
    f.close()

    fileLists.remove(fileLists[0])

    listDictionaries = []
    electoralDistrict = {}
    for i in range(len(fileLists)):
        fileLists[i] = fileLists[i].split(",")
        electoralDistrict["province"] = fileLists[i][0]
        electoralDistrict["districtName"] = fileLists[i][1]
        electoralDistrict["districtNum"] = fileLists[i][2]
        electoralDistrict["districtPop"] = fileLists[i][3]
        electoralDistrict["electors"] = float(fileLists[i][4])
        electoralDistrict["pollingStations"] = fileLists[i][5]
        electoralDistrict["validBallots"] = fileLists[i][6]
        electoralDistrict["percentValidBallots"] = fileLists[i][7]
        electoralDistrict["rejectedBallots"] = fileLists[i][8]
        electoralDistrict["percentRejectedBallots"] = fileLists[i][9]
        electoralDistrict["totalBallots"] = fileLists[i][10]
        electoralDistrict["percentVoterTurnout"] = fileLists[i][11]
        listDictionaries.append(electoralDistrict)
        electoralDistrict = {}
    return listDictionaries

"""
This function takes a district number and displays to the console the number of polling stations
the number of valid ballots, the total ballots cast, and percentage of voter turnout.
Parameters are the data list "dictionaries", and the district number. Does not return
"""
def displayInfo(dictionaries, districtNum):
    newDict = dictionaries
    insertionSort(newDict, "districtNum")
    position = search(newDict, "districtNum", districtNum)

    if not(position == -1):
        print("Electoral District " + str(districtNum) + ":")
        print("Number of polling stations: " + newDict[position]["pollingStations"])
        print("Number of valid ballots: " + newDict[position]["validBallots"])
        print("Total ballots cast: " + newDict[position]["totalBallots"])
        print("Percentage of voter turnout: " + newDict[position]["percentVoterTurnout"])
    else:
        print("This electoral district does not exist!")

"""
This function takes a province and returns a list of the names of the electoral
districts in that province. Parameters are the data list "dictionaries" and a province name.
If province does not exist, it will return an error message.
"""
def uniqueDistricts(dictionaries, province):
    newDict = dictionaries
    insertionSort(newDict, "province")

    districtList = []
    position = search(newDict, "province", province)
    if not(position == -1):
        districtList.append(newDict[position]["districtName"])

        #Searching behind where the search function had found the province position
        i = position - 1
        while newDict[i]["province"] == province:
            districtList.append(newDict[i]["districtName"])
            i -= 1
            
        #Searching in front of where the search function had found the province position
        k = position + 1
        while newDict[k]["province"] == province:
            districtList.append(newDict[k]["districtName"])
            k += 1
        districtList.sort()
        return districtList
    else:
        return "This province does not exist!"

"""
Returns the maximum value for a supplied key value. Parameters are the data list "dictionaries"
and a key value
"""
def findMax(dictionaries, aKey):
    if checkKeys(dictionaries, aKey):
        maxVal = float(dictionaries[0][aKey])
        for i in dictionaries:
            if float(i[aKey]) > maxVal:
                maxVal = float(i[aKey])
        return maxVal
    else:
        return "Search not valid!"

"""
Returns the minimum value for a supplied key value. Parameters are the data list "dictionaries"
and a key value
"""
def findMin(dictionaries, aKey):
    if checkKeys(dictionaries, aKey):
        minVal = float(dictionaries[0][aKey])
        for i in dictionaries:
            if float(i[aKey]) < minVal:
                minVal = float(i[aKey])
        return minVal
    else:
        return "Search not valid!"

"""
Accepts the list of dictionaries as its parameter and returns a list of dictionaries which consists
of the total number of ballots cast in every Canadian province and territory
"""
def totalVotes(dictionaries):
    newDict = insertionSort(dictionaries, "province")
    
    province = newDict[0]["province"]

    #Creates empty dictionary and list to be filled with province data
    totalVotesDict = {}
    totalVotes = []
    totalVoteCount = 0
    for i in newDict:
        if i["province"] == province:
            totalVoteCount = totalVoteCount + int(i["totalBallots"])
        else:
            totalVotesDict["province"] = province
            totalVotesDict["totalVotes"] = totalVoteCount
            totalVotes.append(totalVotesDict)
            totalVotesDict = {}
            province = i["province"]
            totalVoteCount = int(i["totalBallots"])

    #For the last province - since there is no other provinces after and the else will not be activated
    #which would cause the last province to not be added
    totalVotesDict["province"] = province
    totalVotesDict["totalVotes"] = totalVoteCount
    totalVotes.append(totalVotesDict)
    return totalVotes

"""
Accepts the list of dictionaries, and a key as parameters and then sorts the supplied list of dictionaries
in situ into increasing order based on the specified key. Returns the sorted dictionary or
returns an error message if the key is not valid
"""
def insertionSort(dictionaries, aKey):
    if checkKeys(dictionaries, aKey):
        for i in range(1, len(dictionaries)):
            j = i
            while (j > 0) and (dictionaries[j-1][aKey] > dictionaries[j][aKey]):
                dictionaries[j-1], dictionaries[j] = dictionaries[j], dictionaries[j-1]
                j = j - 1
        return dictionaries
    else:
        return "Sort input not valid!"

"""
Accepts the list of dictionaries and a district number as parameters and searches for
an electoral district based on its electoral district number and returns the percentage of
voter turnout in that district
"""
def binarySearch(dictionaries, districtNum):
    newDict = insertionSort(dictionaries, "districtNum")

    position = search(dictionaries, "districtNum", districtNum)
    if not(position == -1):
        percentTurnout = newDict[position]["percentVoterTurnout"]
        return percentTurnout
    else:
        return "This district number does not exist!"

"""
Accepts the list of dictionaries, a key value, and a value to search for
as parameters, and performs a binary search for that value. Returns the position of the value
if found, and -1 if not. Returns an error message if Key is not valid
"""
def search(dictionaries, aKey, aVal):
    if checkKeys(dictionaries, aKey):
        low = 0
        high = len(dictionaries) -1
        while high >= low:
            mid = (high + low) //2
            if (str(aVal) == dictionaries[mid][aKey]):
                return mid
            if (str(aVal) < dictionaries[mid][aKey]):
                high = mid - 1
            else:
                low = mid + 1
        return -1
    else:
        return "Search input not valid!"

"""
Accepts the list of dictionaries and a key value as parameters, and returns True
if the key can be found in the dictionaries, False if not
"""
def checkKeys(dictionaries, aKey):
    if aKey in list(dictionaries[0].keys()):
        return True
    return False

"""
Calls the function to read the data file, and contains testing code that prints the
various function outputs and also prints the output that is supposed to be printed/returned
"""
def main():
    dictionaries = readData("dataset.csv")

    print("Testing, 1, 2, 3", end = "\n")
    print()

    print("displayInfo")
    displayInfo(dictionaries, 1000)
    print()

    print("uniqueDistricts")
    print(uniqueDistricts(dictionaries, "PrinceEdwardIsland"))
    print()

    print("findMax")
    print(findMax(dictionaries, "electors"))
    print()

    print()
    print("findMin")
    print(findMin(dictionaries, "electors"))
    print()

    print()
    print("totalVotes")
    print(totalVotes(dictionaries))
    
    print()
    print("insertionSort")
    insertionSort(dictionaries, "electors")
    for i in range(5):
        print(dictionaries[i])
    print(".")
    print(".")
    print(".")
    for k in range(len(dictionaries)-5,len(dictionaries)):
        print(dictionaries[k])
    print()
    
    print(binarySearch(dictionaries, 10001))
    print(binarySearch(dictionaries, 34567))
main()
