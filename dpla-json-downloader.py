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
folder = 'YOUR_FOLDER_NAME'

# base URL for DPLA api
apiBase = 'https://api.dp.la/v2/items?'

# fields to be provided in the results. In this case: item title, DPLA id, contributing institution, local URI, collection title, and type metadata
# note: the deprecated field, "originalRecord.type" has been removed. This data can no longer be retrieved from the API
fields = 'sourceResource.title,id,dataProvider,isShownAt,sourceResource.collection.title,sourceResource.type'

# variable for API key
apiKey = 'YOUR_API_KEY'

# variable for Service Hub identifier: makes record retrieval more precise if provider names are the same across the DPLA's 1,000s of data sets
hubId = 'YOUR_SERVICE_HUB_ID'

# variable for csv file of provider list --this can be downloaded from DPLA analytics
providerList = 'YOUR_CSV_FILE.csv'

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

with open(providerList, newline='', encoding='utf-8') as csv_file:
  csv_reader = csv.reader(csv_file)

  # begin a for loop that will grab each row of the CSV and strip its whitespace
  for row in csv_reader:
    # strip row of whitespace
    provider = row[0].strip()

    # create API request
    apiRequest = apiBase + 'api_key=' + apiKey + '&fields=' + fields + '&page_size=500&provider.@id=' + '"' + hubId + '"' + '&dataProvider=' + '"' + provider + '"'

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
            jsonDir = folder + '/' + provider + str(1) + '.json'

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

                  jsonDir = folder + '/' + provider + str(x) + '.json'

                  with open(jsonDir, 'wb') as g:
                    g.write(s.content)
        # log error if JSON dataset is empty:
        else:
            print('Error retrieving data for provider: ' + provider)
            emptyError = [[provider,'Data set is empty']]
            errorWriter.writerows(emptyError)
    # log error if data does not exist:
    else:
        print('Error retrieving data for provider: ' + provider)
        existenceError = [[provider,'Data does not exist']]
        errorWriter.writerows(existenceError)
