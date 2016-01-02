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

#############################################    

def main(argv):
       
    parser = argparse.ArgumentParser(description='Enrich json files using the Rosette API')
    parser.add_argument('-o', '--outputdir', default="enriched", help="subdirectory to store the enriched files")
    parser.add_argument('-r', '--responsedir', default="responses", help="subdirectory to store Rosette responses")
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

    # create output directory
    sOutputDir = os.getcwd() + '/' + args.outputdir
    if not os.path.isdir(sOutputDir):
        try:
            os.mkdir(sOutputDir)
        except Exception, e:
            sys.exit(e)

    # create response storage directory
    sResponseDir = os.getcwd() + '/' + args.responsedir
    if not os.path.isdir(sResponseDir):
        try:
            os.mkdir(sResponseDir)
        except Exception, e:
            sys.exit(e)

    for sFile in lstFiles:
        
        # read the input file   
        print "enrich.py: reading:", sFile                      
        try:
            f = open(sFile, 'r')
        except Exception, e:
            print "enrich.py: error opening:", e
            continue
        try:
            jInput = json.load(f)
        except Exception, e:
            print "enrich.py: error reading:", e
            f.close()
            continue
        
        # ASSERT: jInput is valid and populated

        # construct related file paths                
        sOutputFile = sOutputDir + '/' + sFile 
        sResponseFile = sResponseDir + '/' + sFile 
        
        # if there is an existing response file...
        if os.path.isfile(sResponseFile):
            print "enrich.py: using stored response:", sResponseFile
            try:
                fi = open(sResponseFile, 'r')
            except Exception, e:
                print "enrich.py: error opening:", e
                f.close()
                continue
            try:
                jResponse = json.load(fi)
            except Exception, e:
                print "enrich.py: error reading:", e
                fi.close()
                f.close()
                continue
            # jResponse now contains the stored response file...
        else:
            print "enrich.py: sending text to Rosette API..."
            # extract text from the file
            sText = jInput['subject'] + ' ' + jInput['body']
            # to do: strip ascii etc?
            # connect to rosette 
            if not rosette:
                rosette = API(user_key=args.key)
                params = DocumentParameters()
            # send the text
            params['content'] = sText
            jResponse = rosette.entities(params)  # entity linking is turned off
            # write out the response
            print "enrich.py: writing response:", sResponseFile
            try:
                fr = open(sResponseFile, 'w')
            except Exception, e:
                print "enrich.py: error creating:", e
                f.close()
                continue
            try:
                json.dump(jResponse,fr, sort_keys=True, indent=4, separators=(',', ': '))
            except Exception, e:
                print "enrich.py: error writing:", e
                fr.close()
                f.close()
                continue
            # the response file has been written
            fr.close()
        
        # ASSERT: jResponse is valid and populated
            
        # if there is an enriched file...
        if os.path.isfile(sOutputFile):
            print "enrich.py: already enriched:", sOutputFile
        else:
            # filter and invert the response
            dictEntities = {}
            lstEntities = jResponse['entities']
            for entity in lstEntities:
                if float(entity['confidence']) > 0.01:
                    # map the type
                    sType = entity['type'].lower()
                    if ':' in sType:
                        sType = sType.split(':')[1]
                    # enrich the input file JSON structure:
                    lstTmp = []
                    if dictEntities.has_key(sType):
                        # add entity to type
                        lstTmp = dictEntities[sType]
                        lstTmp.append(entity['normalized'])
                        dictEntities[sType] = lstTmp
                    else:
                        # add type
                        lstTmp.append(entity['normalized'])
                        dictEntities[sType] = lstTmp
                        
            for k in dictEntities.iterkeys():
                jInput[k] = dictEntities[k]

            # write the enriched file
            print "enrich.py: writing:", sOutputFile
            try:
                fo = open(sOutputFile, 'w')
            except Exception, e:
                print "enrich.py: error creating:", e
                f.close()
                continue
            try:
                json.dump(jInput,fo, sort_keys=True, indent=4, separators=(',', ': '))
            except Exception, e:
                print "enrich.py: error writing:", e
                fo.close()
                f.close()
                continue
            fo.close()
            
        # close input file
        f.close()
                        
    # end for
    
    print "enrich.py: done"
    
# end main

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end