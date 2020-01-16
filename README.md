# dpla-api-json-downloader

This calls the DPLA-API, using provider titles provided in a CSV and downloads JSON-LD metadata for those collections.

For best results, provider titles listed in the CSV should include plus signs ('+') instead of spaces between words, i.e. 'dataProvider+title' rather than 'dataProvider title'.

To run this script, provide appropriate values for variables near beginning of program, including:

- folder name into which JSON data will be saved
- API key for querying the DPLA API
- Fields you want provided
- ID of a Service Hub
- Name of the csv file with provider titles.

Run script in same directory as the csv file with collection titles.

Note: for the API request, it is not necessary to include 'provider.@id' but this helps to insure data is from the correct service hub in case there are multiple institutions of the same name across DPLA's data. The pre-formatted current request will provide:

- sourceResource.title: the title of the item
- id: the items DPLA ID
- isShownAt: the item's local ID
dataProvider: the contributing institution
- sourceResource.collection.title: the title of the collection of which the record is a part
- originalRecord.type: Deprecated. original Type metadata value harvested by the DPLA. After Ingestion 3, entire original records are provided as a single string and code for extraction will depend on the format of the hub's original records
- sourceResource.type: Type metadata value created by the DPLA which should appear in DPLA search interfaces

Script was built and run on a machine with Python 3.7. Has not been tested on earlier versions of Python
