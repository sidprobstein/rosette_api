===========
rosette-api
===========

Python tools for use with the Basis Technology Rosette API

enrich.py:  sends JSON documents to Rosette API and enriches them with entity extraction


Usage
-----
python enrich.py [-h] [-o OUTPUTDIR] -k KEY filespec
	

Arguments
---------
-h requests help
-o specifies the directory where enriched files are written; the default is enriched
-k specifies the rosette API key, and is required
filespec must be the path to one or more json files 


