#!/usr/local/bin/python2.7
# encoding: utf-8
'''
@author:     Sid Probstein

@copyright:  RightWhen, Inc. All Rights Reserved.

@license:    MIT License (https://opensource.org/licenses/MIT)

@contact:    sid@rightwhen.com
'''

import sys
import os
import argparse
import glob
import json
from rosette.api import API, DocumentParameters

def main(argv):
       
    parser = argparse.ArgumentParser(description='Enrich json files using the Rosette API')
    parser.add_argument('-o', '--outputdir', default="enriched", help="subdirectory into which to place enriched files")
    parser.add_argument('-k', '--key', required=True, help="rosette api key")
    parser.add_argument('filespec', help="path to the json file(s) to enrich")
    args = parser.parse_args()

    # initialize
    lstFiles = []
    rosette = ""
    
    print "enrich.py: starting up..."
   
    if args.filespec:
        lstFiles = glob.glob(args.filespec)
    else:
        sys.exit()

    sOutputDir = os.getcwd() + '/' + args.outputdir
    print "outputdir:", sOutputDir
    if not os.path.isdir(sOutputDir):
        print "mkdir:", sOutputDir
        try:
            os.mkdir(sOutputDir)
        except Exception, e:
            sys.exit(e)

    for sFile in lstFiles:
        
        print "opening:", sFile
                           
        try:
            f = open(sFile, 'r')
        except Exception, e:
            sys.exit(e)
           
        # read the file
        try:
            jData = json.load(f)
        except Exception, e:
            sys.exit(e)
                
        # debug
        # pprint(jData)
        # print jData['from']
        
        sOutputFile = sOutputDir + '/' + sFile 
        
        if os.path.isfile(sOutputFile):
            print "skipping:", sFile, "(already enriched)"
        else:
            # combine
            sText = jData['subject'] + ' ' + jData['body']
            
            # enrich
            
            # connect to rosette if not already done
            if not rosette:
                rosette = API(user_key=args.key)
                params = DocumentParameters()
            
            # entities
            params['content'] = sText
            result = rosette.entities(params)  # entity linking is turned off
            # to do: trim low confidence items
            # add result to jData
            jData[u'entities'] = result

            # categories
            result = rosette.categories(params)  # entity linking is turned off
            # add result to jData
            jData[u'categories'] = result

            # sentiment
            result = rosette.sentiment(params)  # entity linking is turned off
            # add result to jData
            jData[u'sentiment'] = result
            
            # write out
            
            print "creating:", sOutputFile
            try:
                fo = open(sOutputFile, 'w')
            except Exception, e:                # to do: clean up
                f.close()
                sys.exit(e)
            print "writing:", sOutputFile
            # write the file
            try:
                json.dump(jData,fo)
            except Exception, e:
                sys.exit(e)
            fo.close()
                        
        f.close()
                        
    # end for
    
    print "enrich.py: done"
    
# end main

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end