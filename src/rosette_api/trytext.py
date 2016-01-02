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
import json
import pprint
from rosette.api import API, DocumentParameters

#############################################    

def main(argv):
       
    parser = argparse.ArgumentParser(description='Enrich text with the Rosette API')
    parser.add_argument('-k', '--key', required=True, help="rosette api key")
    args = parser.parse_args()

    # initialize
    rosette = ""
    
    print "trytext.py: starting up..."
    
    ##########
    # extract text from the file
    sText = "\"Gigli\" -- which spawned the phenomenon the gossip pages and celebrity magazines so lovingly refer to as \"Bennifer\" -- is every bit as unwatchable as the deafening negative chatter would suggest. The dialogue from writer-/sdirector Martin Brest is clunky, the film has serious tonal inconsistencies and at more than two hours, it drags on way longer than it should. Even making a little game of it, and trying to pinpoint the exact moment when Ben Affleck and Jennifer Lopez fell in love, stops being fun after a while. Perhaps it\'s when he says, in an attempt to seduce her, \"I\'m the bull, you\'re the cow.\" Or when she beckons him into foreplay by lying back in bed and purring, \"Gobble, gobble\" -- which could forever change the way you view your Thanksgiving turkey. But as pop-star vehicles go, \"Gigli\" isn\'t as insufferable as, say, last year\'s Madonna-Guy Ritchie debacle, \"Swept Away.\" It\'s more on par with Mariah Carey\'s \"Glitter\" and Britney Spears\' \"Crossroads.\" If this were a movie starring two B-list actors, or two complete unknowns, it probably would have gone straight to video. After curious masochists and J.Lo fans check it out the first weekend, \"Gigli\" probably will have a drop-off in audience that rivals \"The Hulk\" -- 70 percent -- then go to video. And with the release next spring of Kevin Smith\'s \"Jersey Girl,\" in which they also co-star, we can have this little conversation all over again. For now, we have Affleck starring as incompetent mob thug Larry Gigli. (That\'s pronounced JEE-lee, which rhymes with really, a running joke that isn\'t particularly funny the first time.) Gigli is asked to kidnap Brian (Justin Bartha), the mentally disabled younger brother of a/sfederal prosecutor who\'s going after a New York mobster (Al Pacino). His boss, however, thinks he\'s incapable of handling the assignment alone and sends in Ricki (Lopez), another contractor, to help him. Gigli is an anti-social lout who lives in a seedy apartment. Ricki is beautiful, grounded, enlightened. She quotes Sun Tzu -- who could blame Gigli for falling for her? (And whether you like her or not, Lopez does have an undeniable presence.) But Ricki is also a lesbian -- so it makes absolutely no sense when she falls for him, too, although they have all the obligatory banter and alleged sexual tension required of a romantic comedy. (And it\'s only a romantic comedy sometimes. Other times, it aims to be an edgy action-crime movie; still other times, it aspires for gag-inducing poignancy.) Apparently, the only force that binds them is the fact that they both feel squeamish about cutting off Brian\'s thumb and mailing it to his prosecutor brother. Instead, they break into a morgue and saw the thumb off a corpse using a plastic knife, while Brian -- who has an unexplained penchant for old-school rap -- sings Sir Mix-a-Lot\'s \"Baby Got Back.\" It\'s also incredibly misinformed to suggest that Ricki can be \"converted\" to heterosexuality -- that a man\'s love is all she really needed to allay any confusion about all that silly lesbian stuff. So what you have here is \"Rain Man\" meets \"Chasing Amy\" -- which is apropos, since the latter is a 1997 Kevin Smith movie in which Affleck also starred as a guy who falls for a lesbian. Instead of counting matches and obsessing about \"The People\'s Court\" like Dustin Hoffman\'s \"Rain Man\" character, Brian counts sunflower seeds and obsesses over going to \"the Baywatch.\" Cameos from Pacino, Christopher Walken as a detective and Lainie Kazan as Gigli\'s mother don\'t help, either. Did they owe someone a favor? What are they doing here? Pacino won his one and only Oscar with Brest for 1992\'s \"Scent of a Woman,\" but couldn\'t he have just thanked the director instead? Instead, we get to see Pacino shoot someone in the head, then watch as fish in a nearby aquarium snack on splattered drops of the victim\'s blood."
    ##########
    # to do: strip ascii etc?
    # connect to rosette 
    if not rosette:
        rosette = API(user_key=args.key)
        params = DocumentParameters()
    # send the text
    params['content'] = sText
    jResponse = rosette.entities(params)  # entity linking is turned off
    print json.dumps(jResponse, sort_keys=True, indent=4, separators=(',', ': '))
    jResponse = rosette.sentiment(params)  # entity linking is turned off
    print json.dumps(jResponse, sort_keys=True, indent=4, separators=(',', ': '))
     
    print "trytext.py: done"
    
# end main

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end