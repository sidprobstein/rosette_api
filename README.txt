===========
rosette-api
===========

Python tools for use with the Basis Technology Rosette API

enrich.py: Enrich json files using the Rosette API'


Usage
-----
python enrich.py [-h] [-o OUTPUTDIR] [-r RESPONSEDIR] -k KEY filespec
	

Arguments
---------
-o specifies the subdirectory where enriched files are written; default: enriched
-r specifies the subdirectory where responses from Rosette API are saved; default: 
responses
-k specifies the rosette API key
filespec must be the path to one or more json files 


Operation
---------
Enrich.py iterates through each json file, takes the fields "subject" and "body",
combines them, and sends them to Rosette API for entity extraction. (This will
be specified on the CLI in a future version.)

The response from Rosette is written out to a file of the same name, in the response 
subdirectory. 

Enrich.py then filters the entities to those with confidence > 0.1 and groups
them into lists by type. Finally, it merges those types with the input file, and 
writes the enriched file into the enriched subdirectory.

Enrich.py will automatically use a saved response file instead of calling Rosette API.
This allows you to modify the filtering and representation of the response without
incurring charges. Just delete the enriched file before running enrich.py.

If you want to get a new response file from Rosette API, delete the response file.
It only makes senes to do this if your input file has changed, or Rosette has.


Notes
-----
Only Entity Extraction is currently supported.


