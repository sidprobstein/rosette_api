#!/usr/local/bin/python2.7
# encoding: utf-8
'''
@author:     Sid Probstein
@license:    MIT License (https://opensource.org/licenses/MIT)
@contact:    sidprobstein@gmail.com
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
    parser.add_argument('-f', '--fieldlist', action="append", help="list of fields to send for enrichment")
    parser.add_argument('-k', '--key', required=True, help="rosette api key")
    parser.add_argument('filespec', help="path to the json file(s) to enrich")
    args = parser.parse_args()

    # initialize
    lstFiles = []
    rosette = ""
       
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
        
        # if no existing response file...
        if not os.path.isfile(sResponseFile):
            # send to Rosette...
            print "enrich.py: sending text to Rosette API..."
            # extract text from the file
            sText = ""
            for field in args.fieldlist:
                sText = sText + jInput[field] + ' '
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
        else:
            # use the stored response
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
        
        # ASSERT: jResponse is valid and populated
        
        # success reading
        f.close()
            
        # filter/map entities
        dictEntities = {}
        lstEntities = jResponse['entities']
        for entity in lstEntities:
            # entity confidence threshold
            if float(entity['confidence']) > 0.01:
                # invert type:entity to dict[type]=[entity1, entity2]
                sType = entity['type'].lower()
                if ':' in sType:
                    sType = sType.split(':')[1]
                lstTmp = []
                if dictEntities.has_key(sType):
                    # add entity to type
                    lstTmp = dictEntities[sType]
                    lstTmp.append(entity['normalized'])
                    dictEntities[sType] = lstTmp
                else:
                    # add type and first entity
                    lstTmp.append(entity['normalized'])
                    dictEntities[sType] = lstTmp
        # done filtering/mapping entities            
        # add types to input structure            
        for key in dictEntities.iterkeys():
            jInput[key] = dictEntities[key]
            
        # if there is no enriched file...
        if not os.path.isfile(sOutputFile):
            # write the enriched file
            print "enrich.py: writing:", sOutputFile
            try:
                fo = open(sOutputFile, 'w')
            except Exception, e:
                print "enrich.py: error creating:", e
                continue
            try:
                json.dump(jInput, fo, sort_keys=True, indent=4, separators=(',', ': '))
            except Exception, e:
                print "enrich.py: error writing:", e
                fo.close()
                continue
            # success writing
            fo.close()
        else:
            # an enriched file already exists
            print "enrich.py: already enriched:", sOutputFile, "output would be:"
            # so, print the result
            print json.dumps(jInput, sort_keys=True, indent=4, separators=(',', ': '))
                                    
    # end for
    
# end main

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end