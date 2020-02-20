@rem test nmake and check errorlevel
cl
if "%ERRORLEVEL%" neq "9009" goto :done

if exist "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat" goto vc2015x64
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars32.bat" goto vc2017x64
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars32.bat" goto vc2019x64
call "C:\Program Files\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat"
SET CL=/arch:IA32 /D "_USING_V110_SDK71_"
goto done
:vc2015x64
call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat"
SET CL=/arch:IA32 /D "_USING_V110_SDK71_"
goto done
:vc2017x64
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars32.bat"
SET CL=/arch:IA32
:vc2019x64
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars32.bat"
SET CL=/arch:IA32
:done
