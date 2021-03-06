# pytoggl

* pytoggl.py: simple wrapper for the Toggl REST-API
* addTogglTag.py: script to add a tag to an entry
* post-commit: git-hook example to add current branch as a tag

## Use case for the git-hook
The raison d'etre of this whole thing is to remember what branches
have been getting some keyboardtime

For instance, On certain git-hooks you can send the branchname to Toggl.
If there is a running entry, add the tag to that entry.
If there isn't, create an entry with the tag.

**Don't forget to add your API-token**

You can obviously send something else, on a different trigger.
See the `addTogglTag.py` use case for that

## Use case for addTogglTag
You can call this on any trigger with any tagname

**Don't forget to add your API-token**


	usage: addTogglTag.py [-h] [-v] -t TAG [-w WORKSPACE] [-n ENTRYDNAME]
	                      [--dontcreate]

	Add tags to running Toggl entries: will create a new one if none is running

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --verbose         Increase output verbosity
	  -t TAG, --tag TAG     The name of the tag to add
	  -w WORKSPACE, --workspace WORKSPACE
	                        The name of the workspace a new entry is started in;
	                        default is the first encountered
	  -n ENTRYDNAME, --entrydname ENTRYDNAME
	                        The name used for an entry, if a new one is created;
	                        has no meaning when supplied with --dontcreate default
	                        is 'Entry started by addTogglTag script'
	  --dontcreate          Don't create a new entry if none is running


## Use case for the PyToggl class
While it could be seen as (the start of) an API wrapper, currently the
clearest usecase would be "used in addTogglTag" :)

Usage:

    pt = PyToggl(token)
    pt.setVerbose(verbose)
    current = pt.getCurrent()

# Also
* See licence.txt
* I'm so not a python programmer.
Gimme a shout if I did something stupid or
when you have some tips :)
