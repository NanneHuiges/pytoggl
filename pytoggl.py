#!/usr/bin/env python
"""Wrapper-like module for using the Toggl API

The module pytoggl is made to support the simple
addTogglTag script, but can serve other purposes and
can easily be expanded into a complete wrapper I hope.

Functionality is exposed via the class PyToggl.
Usage, e.g. get the currently running entry:

pt = PyToggl(yourapitoken)
current = pt.getCurrent()

author: Nanne Huiges
email: nanne@huiges.nl
"""

import requests, json


class PyToggl:
  """A simple wrapper for the Toggl REST API"""

  _log = []
  _token = None
  _baseurl = "https://www.toggl.com/api/v8/"
  _verbose = False

  def __init__(self, token):
    self._token = token

  def setVerbose(self, verbose):
    """Prints the log messages during execution"""
    self._verbose = verbose

  def getLog(self):
    """Returns the log. The log gets set even if verbose is off"""
    return self._log
    
  def _logMsg(self, msg):
    if self._verbose:
      print msg
    self._log.append(msg)

  def _get(self, url):
    r = requests.get(self._baseurl+url, auth=(self._token, 'api_token')) 
    if not r.status_code == 200:
      return False
    return json.loads(r.text)  

  def _post(self, url, data):
    r =  requests.post(self._baseurl+url, data, auth=(self._token, 'api_token'))
    if not r.status_code == 200:
      return False
    return json.loads(r.text)  

  def _put(self, url, data):
    r =  requests.put(self._baseurl+url, data, auth=(self._token, 'api_token'))     
    if not r.status_code == 200:
      return False
    return json.loads(r.text)  

  def getCurrent(self):
    """Get the currently running entry, if any
    Returns false on error, None if nothing is running
    and the entry if there is one.
    """
    self._logMsg('Getting current entry')
    current = self._get("time_entries/current")
    if not current:
      self._logMsg("Could not retrieve running entry.")
      return False

    if current['data'] is None:
      self._logMsg("No running entry.")
      return None

    self._logMsg('Entry found')
    return current['data']


  def getWorkspace(self, name=None):
    """Get the workspace with specified name, or get the first one
    Returns false on error, or returns a workspace
    """
    self._logMsg('Retrieving workspaces')
    spaces = self._get("workspaces")
    if not spaces:
        self._logMsg("Could not find workspaces. Exiting")
        return False

    if name is None:
        self._logMsg('Using first workspace: '+spaces[0]['name'])
        return spaces[0]
    
    #specified a workspace  
    for space in spaces:
        if space['name'] == name:
            self._logMsg('Found specified workspace '+ name)
            return space

    self._logMsg("specified workspace "+name+" not found.")
    return False

  def createTag(self, wid, name):
    """Create a tag (or ignore if already created)
    Returns false if tags cannot be retrieved, or tag cannot be made.
    otherwise returns (new/found) the tag
    """
    self._logMsg('Creating tag '+name+', if needed')
    tags = self._get("workspaces/"+str(wid)+"/tags")
    if not tags:
      self._logMsg('Cannot retreive workspace tags')
      return False

    for tag in tags:
      if tag['name'] == name:
        self._logMsg('Tag already available')
        return tag  
    
    self._logMsg('New tag. Creating') 
    data = json.dumps({"tag":{"name":name,"wid":wid}})
    tag = self._post("tags", data)
    if not tag:
        self._logMsg('Creating tag failed')
        return False

    self._logMsg('Tag created')
    return tag['data']  

  def createEntry(self, wid, description):
    """Create a new entry
    Starts a new entry with provided description
    in provided workspace.
    """
    self._logMsg('Creating entry');
    data = json.dumps({"time_entry":
      {"description":description,
      "wid":wid, 
      "created_with":"PyToggl"}
      })      
    entry = self._post('time_entries/start', data)
    if not entry:
      self._logMsg('Could not start entry')
      return False

    self._logMsg('Entry started')
    return entry['data']
  

  def addTagToEntry(self, entry, name):
    """Adds a tag to an entry"""
    self._logMsg('Adding tag to entry');
    tags = entry['tags']
    tags.append(name) 
    data = json.dumps({"time_entry":{"tags":tags}})    
    res = self._put("time_entries/"+str(entry['id']),data)
    if not res:
      self._logMsg('Adding tag failed')
      return False

    self._logMsg('Tag added')
    return True
