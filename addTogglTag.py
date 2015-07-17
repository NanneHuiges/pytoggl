#!/usr/bin/env python
"""Simple script to add a tag to a Toggle entry

Adds a tag to the currently running time-entry.
If there is no running entry, one can be created.
Set your API-key below and call with -h for help on options.
"""

import sys
import argparse
from pytoggl import PyToggl
######################################
# Add your token here                #
# Find it on the website:            #
# https://www.toggl.com/app/profile  #
######################################

token = ""
entryName = "Entry started by addTogglTag script"

###################################################
#        No changes needed below this line        #
###################################################

# internal vars reflecting commandline args
verbose = False
tagname = None
workspace = None
create = True


def parseArguments():
    """Parse the commandline arguments, and set the globals to reflect them """
    global verbose, tagname, workspace, create
    parser = argparse.ArgumentParser(
        description='Add tags to running Toggl '
                    'entries: will create a new one if none is running')
    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity",
                        action="store_true")
    parser.add_argument("-t", "--tag",
                        help="The name of the tag to add",
                        required=True)
    parser.add_argument("-w", "--workspace",
                        help="The name of the workspace a new entry is "
                             "started in; default is the first encountered")
    parser.add_argument("-n", "--entrydname",
                        help="The name used for an entry, "
                             "if a new one is created; "
                             "has no meaning when supplied with --dontcreate "
                             "default is '"+entryName+"'")
    parser.add_argument("--dontcreate",
                        help="Don't create a new entry if none is running",
                        action="store_true")
    args = parser.parse_args()
    verbose = args.verbose
    tagname = args.tag
    workspace = args.workspace
    if args.dontcreate:
        create = False


def log(msg):
    if verbose:
        print msg


#################################################
def main():
    parseArguments()
    pt = PyToggl(token)
    pt.setVerbose(verbose)

    current = pt.getCurrent()
    if current is False:
        log('Entry-retrieval went wrong. Exit!')
        return 1

    if current is None:
        if not create:
            # no running entry & specified not to create one. We're done
            log('No running entry and not creating one per request. Finished!')
            return 0

      #start new entry
    workspace = pt.getWorkspace()
    if not workspace:
        log('Cannot find a workspace to create entry in. Exit!')
        return 1

    #create entry
    current = pt.createEntry(workspace['id'], entryName)
    if not current:
        log('Failed creating a workspace. Exit!')
        return 1

    # Entry is running
    tag = pt.createTag(current['wid'], tagname)
    if not tag:
        log('Failed finding or creating the tag. Exit!')
        return 1

    return pt.addTagToEntry(current, tag['name'])

if __name__ == "__main__":
    exit(main())
