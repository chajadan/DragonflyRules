"""
Executing this script directly will instantiate code based off the config file.
"""

from config import *

deployBatContent = r"""REM the following line is a safeguard to protect others from accidental directory content deletion

if %%COMPUTERNAME%% == %(computerName)s (
del /Q %(macroHomeFolder)s
)

if %%COMPUTERNAME%% == %(computerName)s (
xcopy %(macroSourceFolder)s %(macroHomeFolder)s /Y /EXCLUDE:%(macroSourceFolder)s\deployExclude.txt
)

if not %%COMPUTERNAME%% == %(computerName)s (
echo This file needs to be edited to remove/address the file system deletion safeguard
)""" % locals()

def writeDeployBat():
    f = open("deploy.bat", "w")
    f.write(deployBatContent)
    f.close

if __name__ == "__main__":
    writeDeployBat()