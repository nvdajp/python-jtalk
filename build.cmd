@echo off
set _M=%1
if not "%_M%"=="" (
  nmake /f all.mak MACHINE=%_M%
) else (
  nmake /f all.mak
)
