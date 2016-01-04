===========
rosette-api
===========

Python tools for use with the Basis Technology Rosette API

enrich.py: Enrich json files
trytext.py: Template for storing/analyzing responses from Rosette APIs


enrich.py
----------
python enrich.py [-h] [-o OUTPUTDIR] [-r RESPONSEDIR] -k KEY filespec
	
Arguments
---------
-o OUTPUTDIR specifies the subdirectory where enriched files are written; default: 
'enriched'
-r RESPONSEDIR specifies the subdirectory where responses from Rosette API are saved; 
default: 'responses'
-f specifies one or more text field(s) in the json to pass to Rosette API 
-k specifies the rosette API key
filespec must be the path to one or more json files 

Example
-------
python enrich.py -k 12345 -f subject -f body *.json

Operation
---------
Enrich.py iterates through each input file, combines specified fields and sends 
them to Rosette API for entity extraction. (The fields will be specified on the 
CLI in a future version.) The response from Rosette is written out to a file of 
the same name as the input file, but located in the response subdirectory. 

Enrich.py then filters the entities to those with confidence > 0.1 and groups
them into lists by type. Finally, it merges those lists with the input file, and 
writes the result into the enriched subdirectory.

Enrich.py will not overwrite a saved response or a file in the enriched subdirectory. 
This is intended to allow modification of filtering and mapping logic (starting 
with '# filter/map entities' in the module) without calling Rosette API live each 
time. Delete the enriched file after making modifications to make enrich.py create 
a new version using the saved response. 

To obtain an updated response from Rosette API, delete the response file. Note that 
it only makes sense to do this if your input file has changed -- or Rosette has.

Notes
-----
* Only Entity Extraction is currently supported, use TryText.py to explore others


trytext.py
----------
python trytext.py -k KEY
    
Arguments
---------
-k specifies the rosette API key

Notes
-----
* Review the code to see how to change the sample text and analyze the response


