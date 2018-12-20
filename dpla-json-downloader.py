"""
    Creator: Joshua Lynch
    Date: 2018-11
    Description: script designed for metadata retrieval and inspection. Gathers JSON data using the Digital Public Library of America (DPLA) API. This data will be plugged into OpenRefine for inspection
"""
import os
import csv
import requests
import math
import sys
import shutil

# variable for folder that will contain collections' metadata
folder = 'idhhAllCollections'

# variable for API key
apiKey = 'YOUR_API_KEY'

# variable for Service Hub name. It is recommended to use plus signs '+' instead of spaces between words in the hub name, as demonstrated below
serviceHub = 'Service+Hub+Name'

# variable for error log file name
eLog = 'errors.csv'

# catch a folder that already exists in the directory with the same name. Prompt user for action
if os.path.exists(folder):
    decision = input('The folder, "' + folder + '", already exists. Would you like to overwrite it? y/n\n')
    if decision == 'y' or decision == 'Y':
        shutil.rmtree(folder)
    elif decision == 'n' or decision == 'N':
        print('Goodbye.')
        sys.exit()
    else:
        print('Keyboard input not recognized. Goodbye.')
        sys.exit()
        
os.makedirs(folder)

# create an error log that will be populated if there are problems with the website interaction
if os.path.exists(eLog):
    os.remove(eLog)
    
errorLog = open(eLog, 'w', newline='')
errorWriter = csv.writer(errorLog)
errorLogColumnNames = [['collection','error']]
errorWriter.writerows(errorLogColumnNames)

with open('idhhAllCollections.csv', newline='', encoding='utf-8') as csv_file:
  csv_reader = csv.reader(csv_file)
  
  # begin a for loop that will grab each row of the CSV and strip its whitespace
  for row in csv_reader:
    # strip row of whitespace
    collection = row[0].strip()
    
    """ 
        create API request. Note: it is not necessary to include 'provider.name' but this helps to insure data is from the correct service hub in case there are problems with the collection name. The request below will provide:
        sourceResource.title: the title of the item
        dataProvider: the contributing institution
        sourceResource.collection.title: the title of the collection of which the record is a part
        originalRecord.type: original Type metadata value harvested by the DPLA
        sourceResource.type: Type metadata value created by the DPLA which should appear in DPLA search interfaces
    """
    apiRequest = 'https://api.dp.la/v2/items?api_key=' + apiKey + '&fields=sourceResource.title,dataProvider,isShownAt,sourceResource.collection.title,originalRecord.type,sourceResource.type&page_size=500&provider.name=' + serviceHub + '&sourceResource.collection.title=' + '"' + collection + '"'
    
    
    # make request
    r = requests.get(apiRequest)
    
    # check to make sure data exists:
    if (r.status_code == 200):
        # read the JSON file and check for the value of 'count':
        requestData = r.json()

        itemCount = requestData['count']

        # test to make sure API is not returning an empty set:
        if (itemCount > 0):
            #create variable for folder and json file
            jsonDir = folder + '/' + collection + str(1) + '.json'

            # download files
            with open(jsonDir, 'wb') as f:
              f.write(r.content)
            
            """
                The following deals with the DPLA API's record limit of 500 results per page, identifying sets with more than 500 records and advancing pages the appropriate number of times
            """
            
            # if count is larger than 500:
            if itemCount > 500:
                # divide count by 500 rounded up and save as variable for a stopping point of a loop, below
                pages = math.ceil(itemCount / 500)

                # loop that iterates for each page in a big data set
                for x in range(2, (pages + 1)):
                  apiPages = apiRequest + '&page=' + str(x)
                  s = requests.get(apiPages)
                  
                  jsonDir = folder + '/' + collection + str(x) + '.json'
                  
                  with open(jsonDir, 'wb') as g:
                    g.write(s.content)
        # log error if JSON dataset is empty:
        else:
            print('Error retrieving data for collection: ' + collection)
            emptyError = [[collection,'Data set is empty']]
            errorWriter.writerows(emptyError)
    # log error if data does not exist:
    else:
        print('Error retrieving data for collection: ' + collection)
        existenceError = [[collection,'Data does not exist']]
        errorWriter.writerows(existenceError)