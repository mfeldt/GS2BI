#!/usr/bin/env python2
"""

HOW TO TURN GROUPS TO BUILDING INSTRUCTIONS

gs2bi operates on lxfml files saved by LDD!  The grouping information is
used to generate ordered building instructions (BIs), essentially giving
you full control over the BIs.  In order to make full (good, or even any)
use of gs2bi, you must:

  - split your model into groups in LDD. these groups must
    - cover each and every part of your model
    - groups can contain subgroups, but those that do MUST NOT
      contain any additional non-subgrouped parts!
  - save your model in lxfml format!

To generate BIs, gi2bs goes backwards through the groups, while LDD
puts groups in the order they were created.  So it makes sense to
"deconstruct" your model, i.e. first create a group of the very last
parts added, use the hide tool to render these invisible, groupd the
second last added parts into a group etc. Same goes for sub-groups!

If this sounds a bit confusing and complicated, try watching this tutorial:
https://www.youtube.com/xxx

(c) 2019 Markus Feldt <mfeldt@mpia.de>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


"""

import xmltodict
import sys
import argparse


parser = argparse.ArgumentParser(description='Turn LDD grouping information into well-ordere building instructions', epilog=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('infile', metavar='INFILE (lxfml)', type=str, nargs=1, help='input file')
parser.add_argument('outfile', metavar='OUTFILE', type=str, nargs='?', default=None,help='output file, if not present output will be printed to console!')

args = parser.parse_args()


##
##
## handling of BI step printing
##
##
def print_step_begin(steplevel,stepnum):
    level = steplevel.count('Substep')
    idstr = '    '+' '*2*level
    print idstr+'<Camera cameraRef="1"/>'
    print idstr+'<Step name="%s%s">' % (steplevel,stepnum)

def print_step_end(steplevel):
    level = steplevel.count('Substep')
    idstr = '    '+' '*2*level
    print idstr+'</Step>'

def print_step(steplevel,stepnum,refs):
    level = steplevel.count('Substep')
    print_step_begin(steplevel,stepnum)
    print_part_refs(groupsys['Group']['@partRefs'],indent=8+2*level)
    print_step_end(steplevel)

def print_part_refs(refs,indent=8):
    for ref in refs.split(','):
        print " "*indent,'<PartRef partRef="%s"/>' % ref

##
##
## The whole magic of group handling is in this recursive thingy...
##
##

def handle_group(group,steplevel):
    if group.has_key('Group'):
	if group.has_key('@partRefs'):
	    if group['@partRefs'] != '':
                raise LookupError("At least one group contains both part references and sub-goups!")
        if isinstance(group['Group'],list):
            for i in range(len(group['Group'])-1,-1,-1):
                print_step_begin(steplevel,(i-len(group['Group']))*-1)
                tsteplevel = steplevel + ("%s" % ((i-len(group['Group']))*-1))+"Substep"
                handle_group(group['Group'][i],tsteplevel)
                print_step_end(steplevel)
        else:
            print_step_begin(steplevel,1)
            tsteplevel = steplevel+"1Substep"
            handle_group(group['Group'],tsteplevel)
            print_step_end(steplevel)
    else:
        level = steplevel.count('Substep')
        print_part_refs(group['@partRefs'],indent=8+2*level)

##
##
## main part:
##  read + parse XML file
##  copy everything before original building instructions
##  print the new ones
##  close
##
##

## parse XML
a=xmltodict.parse(open(args.infile[0],'r'))

## read all lines as strings
al = open(args.infile[0],'r').readlines()

## find line with original building instructions
li=['<BuildingInstruction name' in l for l in al]
idx = li.index(True) # line where building instructions start

## extract the group system
groupsys=a['LXFML']['GroupSystems']['GroupSystem']

steplevel="BuildingGuide1Step"

## redirect output to out file if present
orig_stdout = sys.stdout
if args.outfile is not None:
    f = open(args.outfile, 'w')
    sys.stdout = f

## print original content up to building instructions
for l in al[:idx+1]:
    print l,

## generate new BIs from groups
handle_group(groupsys,steplevel)

## close the file and end
print """    </BuildingInstruction>
  </BuildingInstructions>
</LXFML>
"""
sys.stdout = orig_stdout
