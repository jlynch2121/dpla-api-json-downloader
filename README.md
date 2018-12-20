# dpla-api-json-downloader

This calls the DPLA-API, using collection titles provided in a CSV and downloads JSON-LD metadata for those collections.

For best results, collection titles listed in the CSV should include plus signs ('+') instead of spaces between words, i.e. 'collection+title' rather than 'collection title'. 

To run this script, provide appropriate values for variables near beginning of program, including a folder name into which JSON data will be saved, an API key for querying the DPLA API, the name of a Service Hub, and name of the csv file with collection titles. Run script in same directory as the csv file with collection titles.

Note: for the API request, it is not necessary to include 'provider.name' but this helps to insure data is from the correct service hub in case there are problems with the collection name. The current request will provide:
        
sourceResource.title: the title of the item
dataProvider: the contributing institution
sourceResource.collection.title: the title of the collection of which the record is a part
originalRecord.type: original Type metadata value harvested by the DPLA
sourceResource.type: Type metadata value created by the DPLA which should appear in DPLA search interfaces

Script was built and run on a machine with Python 3.7. Has not been tested on earlier versions of Python
