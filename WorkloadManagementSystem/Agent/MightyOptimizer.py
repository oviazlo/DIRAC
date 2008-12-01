########################################################################
# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/WorkloadManagementSystem/Agent/MightyOptimizer.py,v 1.4 2008/12/01 17:36:11 rgracian Exp $


"""  SuperOptimizer
 One optimizer to rule them all, one optimizer to find them, one optimizer to bring them all, and in the darkness bind them.
"""
import time
import os
import threading
from DIRAC  import gLogger, gConfig, gMonitor,S_OK, S_ERROR
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.WorkloadManagementSystem.DB.JobDB         import JobDB
from DIRAC.WorkloadManagementSystem.DB.JobLoggingDB  import JobLoggingDB
from DIRAC.Core.Utilities import Time, ThreadSafe
from DIRAC.Core.Utilities.Shifter import setupShifterProxyInEnv


gOptimizerLoadSync = ThreadSafe.Synchronizer()

class MightyOptimizer(AgentModule):

  __jobStates = [ 'Received', 'Checking' ]

  def initialize(self):
    """ Standard constructor
    """
    self.jobDB = JobDB()
    self.jobLoggingDB = JobLoggingDB()
    self._optimizers = {}
    return S_OK()

  def execute( self ):
    result = self.jobDB.selectJobs(  { 'Status': self.__jobStates  } )
    if not result[ 'OK' ]:
      return result
    jobsList = result[ 'Value' ]
    self.log.info( "Got %s jobs for this iteration" % len( jobsList ) )
    if not jobsList: return S_OK()
    result = self.jobDB.getAttributesForJobList( jobsList )
    if not result[ 'OK' ]:
      return result
    jobsToProcess =  result[ 'Value' ]
    for jobId in jobsToProcess:
      self.log.info( "== Processing job %s == " % jobId  )
      jobAttrs = jobsToProcess[ jobId ]
      jobDef = False
      jobOptimized = False
      jobOK = True
      while not jobOptimized:
        result = self.optimizeJob( jobId, jobAttrs, jobDef )
        if not result[ 'OK' ]:
          self.log.error( "Optimizer %s Job %s: %s" % ( jobId, jobAttrs[ 'MinorStatus' ], result[ 'Message' ] ) )
          jobOK = False
          break
        optResult = result[ 'Value' ]
        jobOptimized = optResult[ 'done' ]
        if 'jobDef' in optResult:
          jobDef = optResult[ 'jobDef' ]
      if jobOK:
        self.log.info( "Finished optimizing job %s" % jobId )
      #ONLY DO 2
      if jobId == 2:
        break
    return S_OK()


  def optimizeJob( self, jobId, jobAttrs, jobDef ):
      result = self._getNextOptimizer( jobAttrs )
      if not result[ 'OK' ]:
        return result
      optimizer = result[ 'Value' ]
      if not optimizer:
        return S_OK( { 'done' : True } )
      if not jobDef:
        result = optimizer.getJobDefinition( jobId, jobDef )
        if not result[ 'OK' ]:
          return result
        jobDef = result[ 'Value' ]
      shifterEnv = False
      if optimizer.am_getParam( 'shifterProxy' ):
        shifterEnv = True
        result = setupShifterProxyInEnv( self.__moduleParams[ 'shifterProxy' ],
                                         self.__moduleParams[ 'shifterProxyLocation' ] )
        if not result[ 'OK' ]:
          return result
      result = optimizer.checkJob( jobId, jobDef[ 'classad' ] )
      if not result[ 'OK' ]:
        return result
      if shifterEnv:
        del( os.environ[ 'X509_USER_PROXY' ] )
      nextOptimizer = result[ 'Value' ]
      #Check if the JDL has changed
      newJDL = jobDef[ 'classad' ].asJDL()
      if newJDL != jobDef[ 'jdl' ]:
        jobDef[ 'jdl' ] = newJDL
      #If there's a new optimizer set it!
      if nextOptimizer:
        jobAttrs[ 'Status' ] = 'Checking'
        jobAttrs[ 'MinorStatus' ] = nextOptimizer
        return S_OK( { 'done' : False, 'jobDef' : jobDef } )
      return S_OK( { 'done' : True, 'jobDef' : jobDef } )

  def _getNextOptimizer( self, jobAttrs ):
    if jobAttrs[ 'Status' ] == 'Received':
      nextOptimizer = "JobPath"
    else:
      nextOptimizer = jobAttrs[ 'MinorStatus' ]
    gLogger.info( "Next optimizer for job %s is %s" % ( jobAttrs['JobID'], nextOptimizer ) )
    if nextOptimizer in self._optimizers:
      return S_OK( self._optimizers[ nextOptimizer ] )
    return self.__loadOptimizer( nextOptimizer )

  @gOptimizerLoadSync
  def __loadOptimizer( self, optimizerName ):
    #Need to load an optimizer
    gLogger.info( "Loading optimizer %s" % optimizerName )
    try:
      agentName = "%sAgent" % optimizerName
      optimizerModule = __import__( 'DIRAC.WorkloadManagementSystem.Agent.%s' % agentName,
                              globals(),
                              locals(), agentName )
      optimizerClass = getattr( optimizerModule, agentName )
      optimizer = optimizerClass( "WorkloadManagement/%s" % agentName, self.am_getParam( 'fullName' ) )
      result = optimizer.am_initialize( self.jobDB, self.jobLoggingDB )
      if not result[ 'OK' ]:
        return S_ERROR( errorMsg = "Can't initialize optimizer %s: %s" % ( optimizerName, result[ 'Message' ] ) )
    except Exception, e:
      gLogger.exception( "LOADERROR" )
      return S_ERROR( "Can't load optimizer %s: %s" % ( optimizerName, str(e) ) )
    self._optimizers[ optimizerName ] = optimizer
    return S_OK( optimizer )




