.. _ConfigurationServer:

Systems / Configuration / <INSTANCE> / Service / Server - Sub-subsection
========================================================================

In this subsection the Server service is configured. The attributes are showed in the following table:

+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| **Name**                           | **Description**                            | **Example**                                                             |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *HandlerPath*                      | Relative path directory where the          | HandlerPath = DIRAC/ConfigurationSystem/Service/ConfigurationHandler.py |
|                                    | service is located                         |                                                                         |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *Port*                             | Port where the service is responding       | Port = 9135                                                             |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *UpdatePilotCStoJSONFile*          | Optional flag to enable if you want that   | UpdatePilotCStoJSONFile = True                                          |
|                                    | the configuration on the pilot is dumped   | Default is False                                                        |
|                                    | in a JSON file and uploaded to a webserver |                                                                         |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *pilotFileServer*                  | Web server where to upload the pilot file  | pilotFileServer = lbcertifdirac6.cern.ch                                |
|                                    | and its JSON configuration file            |                                                                         |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *pilotRepo*                        | Pointer to git repository of DIRAC pilot   | pilotRepo = https://github.com/DIRACGrid/Pilot.git                      |
|                                    |                                            | The value above is the default                                          |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *pilotVORepo*                      | Pointer to git repository of VO DIRAC      | pilotVORepo = https://github.com/MyDIRAC/VOPilot.git                    |
|                                    | extension of pilot                         |                                                                         |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *pilotScriptsPath*                 | Path to the code, inside the Git repository| pilotScriptsPath = Pilot                                                |
|                                    |                                            | The value above is the default                                          |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *pilotScriptsVOPath*               | Path to the code, inside the Git repository| pilotScriptsVOPath = VOPilot                                            |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *Authorization*                    | Subsection to configure authorization over | Authorization                                                           |
|                                    | the service                                |                                                                         |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *Authorization/Default*            | Default authorization                      | Default = all                                                           |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *Authorization/commitNewData*      | Define who can commit new configuration    | commitNewData = CSAdministrator                                         |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *Authorization/getVersionContents* | Define who can get version contents        | getVersionContents = CSAdministrator                                    |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
| *Authorization/rollBackToVersion*  | Define who can roll back the configuration | rollBackToVersion = ServiceAdministrator                                |
|                                    | to a previous version                      | rollBackToVersion += CSAdministrator                                    |
+------------------------------------+--------------------------------------------+-------------------------------------------------------------------------+
