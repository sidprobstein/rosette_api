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
                       
    try:
        f = open("enriched/message1.json", 'r')
    except Exception, e:
        sys.exit(e)
       
    # read the response file
    try:
        jData = json.load(f)
    except Exception, e:
        sys.exit(e)

    # entities    
    dictEntities = {}
    lstEntities = jData['entities']['entities']
    for entity in lstEntities:
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

    # categories
    dictCategories = {}
    lstCategories = jData['categories']['categories']
    for category in lstCategories:    
        if float(category['confidence']) < 0.5:
            dictCategories[u'categories'] = category['label'].lower()
    print dictCategories
        
    # sentiment
    dictSentiment = {}
    lstSentiment = jData['sentiment']['sentiment']
    for sentiment in lstSentiment:    
        if float(sentiment['confidence']) < 0.5:
            dictSentiment[u'sentiment'] = sentiment['label']
    print dictSentiment

    f.close()
                    
# end for

print "enrich.py: done"

# end main

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end