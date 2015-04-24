REM the following line is a safeguard to protect others from accidental directory content deletion

if %COMPUTERNAME% == CHAJDESKTOPWIN7 (
del /Q C:\NatLink\NatLink\MacroSystem
)
if %COMPUTERNAME% == CHAJDESKTOPWIN7 (
xcopy C:\Users\chajadan\git\DragonflyRules\DragonflyRules\src C:\NatLink\NatLink\MacroSystem /Y /EXCLUDE:C:\Users\chajadan\git\DragonflyRules\DragonflyRules\src\deployExclude.txt
)

if not %COMPUTERNAME% == CHAJDESKTOPWIN7 (
echo This file needs to be edited to remove/address the file system deletion safeguard
)