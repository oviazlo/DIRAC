""" This is the LHCb Online storage """

from DIRAC import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.DataManagementSystem.Client.Storage.StorageBase import StorageBase
from DIRAC.Core.Utilities.Subprocess import pythonCall
from DIRAC.Core.Utilities.Pfn import pfnparse,pfnunparse
from DIRAC.Core.Utilities.File import getSize
from stat import *
import types,re,os,xmlrpclib

ISOK = True

class LHCbOnlineStorage(StorageBase):

  def __init__(self,storageName,protocol,path,host,port,spaceToken,wspath):
    self.isok = ISOK

    self.protocolName = 'LHCbOnline'
    self.name = storageName
    self.protocol = protocol
    self.path = path
    self.host = host
    self.port = port
    self.wspath = wspath
    self.spaceToken = spaceToken
    self.cwd = self.path
    apply(StorageBase.__init__,(self,self.name,self.path))

    self.timeout = 100

    serverString = "%s://%s:%s" % (protocol,host,port)
    self.server = xmlrpclib.Server(serverString)

  def getParameters(self):
    """ This gets all the storage specific parameters pass when instantiating the storage
    """
    parameterDict = {}
    parameterDict['StorageName'] = self.name
    parameterDict['ProtocolName'] = self.protocolName
    parameterDict['Protocol'] = self.protocol
    parameterDict['Host'] = self.host
    parameterDict['Path'] = self.path
    parameterDict['Port'] = self.port
    parameterDict['SpaceToken'] = self.spaceToken
    parameterDict['WSUrl'] = self.wspath
    return S_OK(parameterDict)

  def isOK(self):
    return self.isok

  def getProtocolPfn(self,pfnDict,withPort):
    """ From the pfn dict construct the SURL to be used
    """
    pfnDict['Path'] = ''
    res = pfnunparse(pfnDict)
    pfn = res['Value'].replace('/','')
    return S_OK(pfn)

  def getFileSize(self,path):
    """ Get a fake file size
    """
    if type(path) == types.StringType:
      urls = [path]
    elif type(path) == types.ListType:
      urls = path
    else:
      return S_ERROR("LHCbOnline.removeFile: Supplied path must be string or list of strings")
    if not len(path) > 0:
      return S_ERROR("LHCbOnline.removeFile: No surls supplied.")
    successful = {}
    failed = {}
    for pfn in urls:
      successful[pfn] = 0
    resDict = {'Failed':failed,'Successful':successful}
    return S_OK(resDict)

  def requestRetransfer(self,path):
    """ Tell the Online system that the migration failed and we want to get the request again
    """
    if type(path) == types.StringType:
      urls = [path]
    elif type(path) == types.ListType:
      urls = path
    else:
      return S_ERROR("LHCbOnline.requestRetransfer: Supplied path must be string or list of strings")
    if not len(path) > 0:
      return S_ERROR("LHCbOnline.requestRetransfer: No surls supplied.")
    successful = {}
    failed = {}
    for pfn in urls:
      try:
        res = self.server.errorMigratingFile(pfn)
        if res:
          successful[pfn] = True
          gLogger.info("LHCbOnline.requestRetransfer: Successfully requested file from Online storage.")
        else:
          errStr = "LHCbOnline.requestRetransfer: Failed to request file from Online storage."
          failed[pfn] = errStr
          gLogger.error(errStr,pfn)
      except Exception,x:
        errStr = "LHCbOnline.requestRetransfer: Exception while requesting file from Online storage."
        gLogger.exception(errStr,lException=x)
        failed[pfn] = errStr
    resDict = {'Failed':failed,'Successful':successful}
    return S_OK(resDict)

  def removeFile(self,path):
    """Remove physically the file specified by its path
    """
    if type(path) == types.StringType:
      urls = [path]
    elif type(path) == types.ListType:
      urls = path
    else:
      return S_ERROR("LHCbOnline.removeFile: Supplied path must be string or list of strings")
    if not len(path) > 0:
      return S_ERROR("LHCbOnline.removeFile: No surls supplied.")
    successful = {}
    failed = {}
    for pfn in urls:
      try:
        res = self.server.endMigratingFile(pfn)
        if res:
          successful[pfn] = True
          gLogger.info("LHCbOnline.getFile: Successfully requested file from Online storage.")
        else:
          errStr = "LHCbOnline.getFile: Failed to request file from Online storage."
          failed[pfn] = errStr
          gLogger.error(errStr,pfn)
      except Exception,x:
        errStr = "LHCbOnline.getFile: Exception while requesting file from Online storage."
        gLogger.exception(errStr,lException=x)
        failed[pfn] = errStr
    resDict = {'Failed':failed,'Successful':successful}
    return S_OK(resDict)
