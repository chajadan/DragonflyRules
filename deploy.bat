REM the following line is a safeguard to protect others from accidental directory content deletion

if %COMPUTERNAME% == CHAJDESKTOPWIN78 (

del /Q C:\NatLink\NatLink\MacroSystem
xcopy . C:\NatLink\NatLink\MacroSystem /Y /EXCLUDE:deployExclude.txt

)

ELSE (

echo This file needs to be edited to remove/address the file system deletion safeguard

)