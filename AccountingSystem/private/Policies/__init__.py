
from DIRAC.AccountingSystem.private.Policies.JobPolicy import JobPolicy

gPoliciesList = {
                 'Job' : JobPolicy(),
                 'WMSHistory' : JobPolicy(),
                 'Pilot' : JobPolicy()
                 }