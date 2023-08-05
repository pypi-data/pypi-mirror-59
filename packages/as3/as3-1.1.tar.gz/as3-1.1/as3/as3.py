''' 
Version 1.0 11th December 2019
Pete White
This is a Python module to simplify operations using F5 AS3
Installation - copy to your python library directory eg /lib/python2.7

https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/userguide/installation.html
https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/index.html

This requires iCR >= 2.4

To Do:
1. Validate against a schema
    - https://pypi.org/project/fastjsonschema/
    - https://pypi.org/project/jsonschema/


'''
###############################################################################
import os
import sys
import time
import json
import requests
import iCR
import fastjsonschema

class as3:
   
  def __init__(self,**kwargs):
    # Setup variables
    # manage keyword arguments
    self.debug = kwargs.pop('debug', False)
    self.host = kwargs.pop('host','127.0.0.1')
    self.username = kwargs.pop('username','admin')
    self.password = kwargs.pop('password','admin')
    self.port = kwargs.pop('port','443')
    self.usetoken = kwargs.pop('usetoken',False)

    # Global variables to hold data
    # self.bigip is the iCR object with which to connect to the BIG-IP
    self.bigip = False
    self.error = ''
  
  def _debug(self,msg):
    """
    Description
    -----------
    This method is a helper function to print debug messages to the console if debugging is turned on ie self.debug = True.
    DEBUG: is prepended to the string in output.
    
    Parameters
    ----------
    msg : string
      The message to be sent to the console
    
    Return: none
    """
    # Function to print debug messages
    if self.debug:
      print("DEBUG: " + msg)
  
  def bigipConnect(self,**kwargs):
    """
    Description
    -----------
    This method is used to connect to the BIG-IP
    
    Parameters
    ----------
    None

    Keywords
    ----------
    host : string. The IP address of the BIG-IP to which you want to connect
    username : string. The username with which you want to connect to the BIG-IP
    password : string. The password you want to use
    usetoken : Boolean. True if you want to use a token to connect, false to use username/password
    port : integer. The TCP port on which the REST service is running

    Return: True on success, False on failure. Sets self.bigip to be the bigip link.
    """
    host = kwargs.pop('host',self.host)
    username = kwargs.pop('username',self.username)
    password = kwargs.pop('password',self.password)
    usetoken = kwargs.pop('usetoken',False)
    port = kwargs.pop('port',self.port)
    # Create the icr connection to the BIG-IP
    bigip = iCR.iCR(host,username,password,port=port,debug=self.debug)

    if usetoken:
      self._debug("Retrieving token")
      bigip.token = bigip.get_token()
      self._debug("Retrieved token: " + str(bigip.token))
      # Handle token retrieval error
      if bigip.token == False:
        self.error = "Cannot retrieve token from host " + host + " with username " + username
        return False
      else:
        self.bigip = bigip
        return True
    if not bigip:
      self.error = bigip.error
      self._debug("BIG-IP connection error:" + bigip.error)
      return False
    else:
      self._debug("BIG-IP connection success")
      self.bigip = bigip
      return True
  
  def github(self,url,**kwargs):
    """
    Description
    -----------
    This is a function used to connect to the F5 Networks AS3 github repository as specified at https://developer.github.com/v3/repos/releases/

    Parameters
    ----------
    url : string. A relative URL without leading slash to show the Github URI eg 'releases/latest'

    Keywords
    --------
    method : string. Default is GET, this allows setting of POST instead, which then requires the data keyword below
    data : dict. Dictionary representing the sent data eg { "name": "myName" }
    useragent : string. The user agent to be used. Default as3
    stream : Boolean, If set to true, the Accept header is set to retrieve stream data
    raw : Boolean. If set to True, retrieve from raw.github.com eg for schemas

    Returns Boolean True or False
    """

    method = kwargs.pop('method','get')
    data = kwargs.pop('data',{})
    useragent = kwargs.pop('useragent','as3')
    stream = kwargs.pop('stream',False)
    raw = kwargs.pop('raw',False)
    # Setup requests settings
    headers = { 'User-Agent': useragent , 'Content-Type': 'application/json' }
    if stream:
      headers['Accept'] = 'application/octet-stream'

    if raw:
      uri = 'https://raw.githubusercontent.com/F5Networks/f5-appsvcs-extension/' + str(url)
    else:
      uri = 'https://api.github.com/repos/F5Networks/f5-appsvcs-extension/' + str(url)
    self._debug("github: URI = " + uri)

    try:
      if method == 'post':
        # Convert the data to JSON
        dataJson = json.dumps(data)
        response = requests.post(uri, data=dataJson, headers=headers, timeout=10)
      else:
        response = requests.get(uri, headers=headers, timeout=10)
    except Exception as e:
      self.error = e
      return False
    self._debug("github: Response code " + str(response.status_code))
    if response.status_code != 200:
      self.error = "Response code is " + str(response.status_code)
      return False
    else:
      if stream:
        # Return an iterable object
        return response.iter_content(chunk_size=1024)
      else:
        return response.text
    
  def installAS3(self,**kwargs):
    """
    Description
    -----------
    This is a function used to install AS3 on a specific device

    Parameters
    ----------
    None

    Keywords
    --------
    version : string. A specific version of the AS3 package eg 3.16.0. This will be retrieved from Github
    filename : string. Specify the RPM file to be installed
    host : string. The BIG-IP to connect to
    username : string. The BIG-IP username to use for connection
    password : string. The BIG-IP password to use for connection
    port : integer. The BIG-IP port to use for connection
    usetoken : boolean. Whether to use a token to connect

    Returns Boolean True or False
    """
    # Allow the user to specify access details, otherwise inherit from the object
    version = kwargs.pop('version',False)
    filename = kwargs.pop('filename',False)
    #
    host = kwargs.pop('host',self.host)
    username = kwargs.pop('username',self.username)
    password = kwargs.pop('password',self.password)
    usetoken = kwargs.pop('usetoken',False)
    port = kwargs.pop('port',self.port)

    # Connect to the BIG-IP if not already done so
    if not self.bigip:
      if not self.bigipConnect(host=host,username=username,password=password,port=port,usetoken=usetoken,debug=self.debug):
        return False

    # Perform touch on file to enable iApps LX
    if not self.bigip.command('touch /var/config/rest/iapps/enable'):
      self.error = "Cannot perform touch on /var/config/rest/iapps/enable"
      return False
    
    # If a filename has been specified then use that
    if filename:
      self._debug("Filename " + filename + " specified, uploading to host " + host)
    elif version:
      # If a version name has been specified then download and use that
      vid = self.versionToId(version)
      if not vid:
        self.error = "Cannot retrieve ID for version " + version + " error: " + str(self.error)
        return False
      filename = self.retrieveVersion(release=vid) 
      if not filename:
        self.error = "Cannot retrieve version " + version + " error: " + str(self.error)
        return False
    else:
      # Otherwise download and install the latest version
      filename = self.retrieveVersion()
      # ToDo: Return the version so it can be checked whether it is installed
      # Download failed
      if not filename:
        self.error = "Cannot retrieve latest version, error: " + str(self.error)
        return False
    # At this point, filename is the name of the local RPM file to upload to the BIG-IP
    # Check that it actually exists
    if not os.path.exists(filename):
      self._debug("ERROR: cannot find file " + filename)
      return False
    self._debug("Uploading file " + filename)
    if not self.bigip.upload(filename):
      self.error = "Upload of file " + filename + " to host " + host + " failed. " + self.bigip.error
    elif self.debug:
      print ("File " + filename + " successfully uploaded to host " + host)
    
    # Install from /var/config/rest/downloads/
    self._debug("Installing package " + filename + " from /var/config/rest/downloads")
    
    data = json.dumps({  "operation": "INSTALL", 
              "packageFilePath": "/var/config/rest/downloads/" + filename
            })
    self.bigip.create('/mgmt/shared/iapp/package-management-tasks',data)
    if self.bigip.code != 202:
      self.error = "request to perform install task for " + filename + " failed: " + self.bigip.error
      return False
    else:
      self._debug("Created task to install package " + filename)
    self._debug("Waiting for 5 secs")
    time.sleep(5)

    # Check the package has actually been installed successfully
    self._debug("Checking whether the package is installed")
    installed = self.isInstalled(host=host,username=username,password=password,usetoken=usetoken,port=port,debug=self.debug)
    if not installed:
      self.error = "Package " + filename + " not installed successfully"
      return False
    else:
      self._debug("Package " + filename + " installed successfully")
      return True

  def uninstallAS3(self,**kwargs):
    """
    Description
    -----------
    This is a function used to uninstall AS3 on a specific device

    Parameters
    ----------
    None

    Keywords
    --------
    host : string. The BIG-IP to connect to
    username : string. The BIG-IP username to use for connection
    password : string. The BIG-IP password to use for connection
    port : integer. The BIG-IP port to use for connection
    usetoken : boolean. Whether to use a token to connect

    Returns Boolean True or False
    """
    # https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/userguide/installation.html#uninstalling-as3
    # Allow the user to specify access details, otherwise inherit from the object
    #
    host = kwargs.pop('host',self.host)
    username = kwargs.pop('username',self.username)
    password = kwargs.pop('password',self.password)
    usetoken = kwargs.pop('usetoken',False)
    port = kwargs.pop('port',self.port)

    # Connect to the BIG-IP if not already done so
    if not self.bigip:
      if not self.bigipConnect(host=host,username=username,password=password,port=port,usetoken=usetoken,debug=self.debug):
        return False
    # Retrieve the current version
    currentVersion = self.isInstalled(host=host,username=username,password=password,usetoken=usetoken,port=port)
    if not currentVersion:
      self.error = "Error retrieving the current version from " + host
      return False
    
    # Uninstall
    if not 'version' in currentVersion or not 'release' in currentVersion:
      self.error = "Cannot find version or release in current version"
      return False
    uri = '/mgmt/shared/iapp/package-management-tasks'
    packageName = "f5-appsvcs-" + currentVersion['version'] + "-" + currentVersion['release'] + ".noarch"
    data = { "operation":"UNINSTALL","packageName": packageName }
    response = self.bigip.create(uri,data)
    if not response:
      self.error = "Error uninstalling package " + packageName
      return False
    time.sleep(5)
    # Confirm it has been removed
    if not self.isInstalled(host=host,username=username,password=password,usetoken=usetoken,port=port):
      return True
    else:
      self.error("Package seems to be uninstalled but cannot be confirmed")
      return False

  def isInstalled(self,**kwargs):
    """
    Description
    -----------
    This is a function check whether the AS3 extension is installed

    Parameters
    ----------
    None

    Keywords
    --------
    version : string. Check for a specific version of the AS3 package eg 3.16.0.
    filename : string. Specify the RPM file to be installed
    host : string. The BIG-IP to connect to
    username : string. The BIG-IP username to use for connection
    password : string. The BIG-IP password to use for connection
    port : integer. The BIG-IP port to use for connection
    usetoken : boolean. Whether to use a token to connect

    Returns the installed version or Boolean True or False
    """
    # Function to check whether the appsvcs AS3 extension is installed
    version = kwargs.pop('version',False)
    #
    host = kwargs.pop('host',self.host)
    username = kwargs.pop('username',self.username)
    password = kwargs.pop('password',self.password)
    usetoken = kwargs.pop('usetoken',False)
    port = kwargs.pop('port',self.port)
    #
    # Connect to the BIG-IP if not already done so
    if not self.bigip:
      if not self.bigipConnect(host=host,username=username,password=password,port=port,usetoken=usetoken,debug=self.debug):
        self._debug("Cannot connect to " + host)
        return False
    response = self.bigip.get('/mgmt/shared/appsvcs/info')
    if not response:
      self._debug("Response from /mgmt/shared/appsvcs/info False")
      return False  
    else:
      self._debug("Response dict => " + str(response))
      if version and 'version' in response and response["version"] != version:
          return False 
      if 'version' in response:
        return response
      else:
        return True

  def versionToId(self,version):
    """
    Description
    -----------
    This is a function to check github and map a version to an ID

    Parameters
    ----------
    None

    Keywords
    --------
    version : string. A the version to retrieve

    Returns id or False
    """
    # Function to map a version name to an ID
    # eg version = 'v3.16.0' and ID is 22093972
    releases = self.github('releases')
    if not releases:
      return False
    else:
      # Loop through all releases and check if name matches the version name
      for release in json.loads(releases):
        self._debug("Release version:" + release['name'] + ', ID:' + str(release['id']))
        if str(release['name']) == str(version):
          return str(release['id'])
      # If the name is not found, return False
      return False

  def retrieveVersion(self,**kwargs):
    """
    Description
    -----------
    This is a function used to retrieve a specific version of the AS3 package

    Parameters
    ----------
    None

    Keywords
    --------
    release : string. A specific version of the AS3 package eg 3.16.0. This will be retrieved from Github

    Returns file name or False
    """
    # Retrieve the release version of AS3 RPM and SHA256 digest from GitHub
    # Also outputs the release notes
    #
    # input = release => Release ID to be retrieved, NOT name eg 123456. Defaults to latest version
    #
    # Allow download of a specific version
    release = kwargs.pop('release', False)
    #
    # If a specific version has not been requested then retrieve the latest version ID and run recursively    
    if not release:
      # Retrieve the release ID for the latest version
      r = self.github('releases/latest')
      if not r:
        # Cannot retrieve the latest version
        return False
      else:
        # Retrieve the latest version and run recursively
        latest = json.loads(r)['id']
        return self.retrieveVersion(release=latest)
    else:
      # Retrieve a specific release ID

      uri = 'releases/' + str(release)
      response = self.github(uri)
      if not response:
        return False

      release = json.loads(response)
      self._debug ("Release version:" + release['name'] + ', ID:' + str(release['id']))
      # Output the release notes below
      body = release['body'].encode('utf-8','replace')
      open ('release-notes-' + release['name'] + '.txt','w').write(body)

      # Loop through the assets for this release
      for file in release['assets']:
        if file['name'].endswith('rpm'):
          self._debug("Downloading file name:" + str(file['name'] + ', Asset ID:' + str(file['id'])))
          response = self.github('releases/assets/' + str(file['id']),stream=True)
          if not response:
            self._debug("Download failed:")
            return False
          else:
            with open (file['name'],'wb') as fd:
              for chunk in response:
                fd.write(chunk)
            return file['name']

  def getSchema(self,**kwargs):
    """
    Description
    -----------
    This is a function to retrieve a schema from github

    Parameters
    ----------
    None

    Keywords
    --------
    version : string. A specific schema version to retrieve

    Returns Boolean True or False
    """
    # Function to retrieve a schema - either the latest or a specific version
    # Latest: https://raw.githubusercontent.com/F5Networks/f5-appsvcs-extension/master/schema/latest/as3-schema.json
    # Specific: https://raw.githubusercontent.com/F5Networks/f5-appsvcs-extension/master/schema/3.16.0/as3-schema.json
    version = kwargs.pop('version',False)
    if version:
      url = 'master/schema/' + str(version) + '/as3-schema.json'
    else:
      url = 'master/schema/latest/as3-schema.json'
    schema = self.github(url,raw=True)
    if not schema:
      self.error = "Cannot retrieve schema from Github URL " + url
      self._debug("Cannot retrieve schema from Github URL " + url)
      return False
    else:
      self._debug("Retrieved schema from Github URL " + url)
      with open ('as3-schema.json','wb') as fd:
        fd.write(schema.encode('utf-8'))
      self._debug('Written file to as3-schema.json')
      return True

  def validateDeclaration(self,declaration,**kwargs):
    """
    Description
    -----------
    This is a function used to validate a declaration against a schema

    Parameters
    ----------
    None

    Keywords
    --------
    version : string. A specific version of the AS3 package eg 3.16.0. This version schema will be retrieved from Github
    schemaFile : string. The local schema file to validate against
    

    Returns Boolean True or False
    """
    # Function to validata a schema 
    version = kwargs.pop('version',False)
    schemaFile = kwargs.pop('schemaFile',False)

    # If schema is not set, retrieve the file
    if not schemaFile:
      # If version is not set, retrieve the latest
      if version:
        if not self.getSchema(version=version):
          self.error = "Error retrieving schema for version " + version
          return False
      else:
        if not self.getSchema():
          self.error = "Error retrieving latest schema"
          return False
        else:
          schemaFile = 'as3-schema.json'
    else:
      self._debug("schemaFile set to " + schemaFile)
      schemaFile = 'as3-schema.json'
    

    # Open the schema file
    try:
      with open(schemaFile,'r') as fd:
        schema = fd.read()
    except Exception as e:
      self.error = "Cannot open schemaFile " + schemaFile + " : " + str(e)
      return False
    
    # Validate that the declaration is valid JSON
    try:
      declaration = json.loads(declaration)
    except Exception as e:
      self.error = "declaration is not valid JSON: " + str(e)
      return False
    
    # Validate that the schema is valid JSON
    try:
      schemaJson = json.loads(schema)
    except Exception as e:
      self.error = "schemaJson is not valid JSON: " + str(e)
      return False
    
    return True
  '''
    # Cannot use the code below at the moment due to a bug with custom formats
    # Validate declaration against the schema

    try:
      fastjsonschema.compile(schemaJson, formats={
        'f5long-id': r'[^\^ \\<>]{0,255}',
        'f5ip': r'[0-9.%]+',
        'f5label': r'.{0,64}',
        'f5remark': r'[^"\\]{0,64}',
        'f5bigip': r'/[ "\\]+',
        'f5base64': r'[a-zA-Z0-9]*',
        'f5pointer': r'[a-zA-Z0-9]*',
        'f5name': r'[a-zA-Z0-9]*',
      })
      fastjsonschema.validate(declaration)
    except fastjsonschema.JsonSchemaException as e:
      self.error = "Validation Failed:" + str(e.message)
      return False
    except fastjsonschema.JsonSchemaDefinitionException as e:
      self.error = "Definition Failed:" + str(e.message)
      return False
    return True
  '''

  def postDeclaration(self,declaration,**kwargs):
    """
    Description
    -----------
    This is a function to post a declaration to a BIG-IP or BIG-IQ

    Parameters
    ----------
    None

    Keywords
    --------
    patch : boolean. Specify whether this is a PATCH or a POST
    host : string. The BIG-IP to connect to
    username : string. The BIG-IP username to use for connection
    password : string. The BIG-IP password to use for connection
    port : integer. The BIG-IP port to use for connection
    usetoken : boolean. Whether to use a token to connect

    Returns response or False
    """
    # /mgmt/shared/appsvcs/declare
    patch = host = kwargs.pop('patch',False)
    host = kwargs.pop('host',self.host)
    username = kwargs.pop('username',self.username)
    password = kwargs.pop('password',self.password)
    usetoken = kwargs.pop('usetoken',False)
    port = kwargs.pop('port',self.port)

    # Validate that the declaration is valid JSON
    try:
      json.loads(declaration)
    except:
      self.error = "declaration is not valid JSON"
      return False
    
    # Connect to the BIG-IP if not already done so
    if not self.bigip:
      if not self.bigipConnect(host=host,username=username,password=password,port=port,usetoken=usetoken,debug=self.debug):
        self._debug("Cannot connect to " + host)
        return False
    # Post the declaration
      response = self.bigip.create('/mgmt/shared/appsvcs/declare',declaration,patch=patch)

    if not response:
      self._debug("Response from /mgmt/shared/appsvcs/declare False")
      return False  
    else:
      self._debug("Response dict => " + str(response))
      return response
  
  def getDeclaration(self,**kwargs):
    """
    Description
    -----------
    This is a function used to retrieve a declaration

    Parameters
    ----------
    None

    Keywords
    --------
    host : string. The BIG-IP to connect to
    username : string. The BIG-IP username to use for connection
    password : string. The BIG-IP password to use for connection
    port : integer. The BIG-IP port to use for connection
    usetoken : boolean. Whether to use a token to connect

    Returns response or False
    """
    # /mgmt/shared/appsvcs/declare
    host = kwargs.pop('host',self.host)
    username = kwargs.pop('username',self.username)
    password = kwargs.pop('password',self.password)
    usetoken = kwargs.pop('usetoken',False)
    port = kwargs.pop('port',self.port)
    
    # Connect to the BIG-IP if not already done so
    if not self.bigip:
      if not self.bigipConnect(host=host,username=username,password=password,port=port,usetoken=usetoken,debug=self.debug):
        self._debug("Cannot connect to " + host)
        return False
    # GET the declaration
    response = self.bigip.get('/mgmt/shared/appsvcs/declare')
    if not response:
      self._debug("Response from /mgmt/shared/appsvcs/declare False")
      return False  
    else:
      self._debug("Response dict => " + str(response))
      return response
  
  def deleteDeclaration(self,**kwargs):
    """
    Description
    -----------
    This is a function used to delete a declaration

    Parameters
    ----------
    None

    Keywords
    --------
    tenantName : string. A specific tenant name to be deleted
    filename : string. Specify the RPM file to be installed
    host : string. The BIG-IP to connect to
    username : string. The BIG-IP username to use for connection
    password : string. The BIG-IP password to use for connection
    port : integer. The BIG-IP port to use for connection
    usetoken : boolean. Whether to use a token to connect

    Returns response dict or False
    """
    # /mgmt/shared/appsvcs/declare
    tenantName = kwargs.pop('tenantName',False)
    host = kwargs.pop('host',self.host)
    username = kwargs.pop('username',self.username)
    password = kwargs.pop('password',self.password)
    usetoken = kwargs.pop('usetoken',False)
    port = kwargs.pop('port',self.port)
    
    # Connect to the BIG-IP if not already done so
    if not self.bigip:
      if not self.bigipConnect(host=host,username=username,password=password,port=port,usetoken=usetoken,debug=self.debug):
        self._debug("Cannot connect to " + host)
        return False
    # Delete the declaration
    if tenantName:
      response = self.bigip.delete('/mgmt/shared/appsvcs/declare/' + str(tenantName))
    else:
      response = self.bigip.delete('/mgmt/shared/appsvcs/declare')
    if not response:
      self._debug("Response from /mgmt/shared/appsvcs/declare False")
      return False  
    else:
      self._debug("Response dict => " + str(response))
      return response
