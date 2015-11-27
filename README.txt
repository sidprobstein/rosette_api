===========
rosette-api
===========

Python tools for use with the Basis Technology Rosette API entity extraction, categorization, sentiment analysis etc. 

Usage
-----

python enrich.py [-h] [-o OUTPUTDIR] -k KEY filespec
	

Arguments
---------

-o specifies the directory where enriched files are written; the default is enriched

-k specifies the rosette API key, and is required

filespec must be the path to one or more json files 


