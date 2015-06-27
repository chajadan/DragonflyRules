REM the following line is a safeguard to protect others from accidental directory content deletion

if %COMPUTERNAME% == CHAJADAN-PC (
del /Q C:\NatLink\NatLink\MacroSystem
)

if %COMPUTERNAME% == CHAJADAN-PC (
xcopy D:\git\DragonflyRules\DragonflyRules\src C:\NatLink\NatLink\MacroSystem /Y /EXCLUDE:D:\git\DragonflyRules\DragonflyRules\src\deployExclude.txt
)

if not %COMPUTERNAME% == CHAJADAN-PC (
echo This file needs to be edited to remove/address the file system deletion safeguard
)