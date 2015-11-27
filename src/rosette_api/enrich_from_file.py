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
import json

def main(argv):
       
    # initialize
    rosette = ""
    
    print "enrich_from_file.py: starting up..."
    print "opening:", "enriched/message3.json"
                       
    try:
        f = open("enriched/message3.json", 'r')
    except Exception, e:
        sys.exit(e)
       
    # read the response file
    try:
        jData = json.load(f)
    except Exception, e:
        sys.exit(e)
    
    dictEntities = {}
    lstEntities = jData['entities']['entities']
    
    for entity in lstEntities:
        print entity
        if float(entity['confidence']) > 0.49:
            # map the type
            sType = entity['type'].lower()
            if dictEntities.has_key(sType):
                # add entity
                if not entity['normalized'] in dictEntities[sType]:
                    dictEntities[sType] = dictEntities[sType] + entity['normalized']
            else:
                # add type
                dictEntities[sType] = entity['normalized']
     
    print dictEntities

    # to do: categories
        
    # to do: sentiment

    f.close()
                    
# end for

print "enrich.py: done"

# end main

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end