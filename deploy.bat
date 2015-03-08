REM the following line is a safeguard to protect others from accidental directory content deletion

if %COMPUTERNAME% == CHAJDESKTOPWIN7 (

del /Q C:\NatLink\NatLink\MacroSystem
xcopy . C:\NatLink\NatLink\MacroSystem /Y /EXCLUDE:deployExclude.txt

)