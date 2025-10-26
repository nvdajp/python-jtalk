@echo off
@rem Setup MSVC build environment. Usage: vcsetup.cmd [x64|x86]
@rem Default is x86 for backward compatibility.

@rem If cl is already available, nothing to do.
cl >NUL 2>&1
if "%ERRORLEVEL%" NEQ "9009" goto :done

setlocal
set ARCH=%1
if /I "%ARCH%"=="x64" goto :detect_x64

@rem ----- x86 toolchain -----
if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars32.bat" goto vc2022x86
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars32.bat" goto vc2019x86
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars32.bat" goto vc2017x86
if exist "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat" goto vc2015x86
goto :done

:vc2022x86
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars32.bat"
SET CL=/arch:IA32
goto :done

:vc2019x86
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars32.bat"
SET CL=/arch:IA32
goto :done

:vc2017x86
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars32.bat"
SET CL=/arch:IA32
goto :done

:vc2015x86
call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat"
SET CL=/arch:IA32 /D "_USING_V110_SDK71_"
goto :done

:detect_x64
@rem ----- x64 toolchain -----
if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" goto vc2022x64
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat" goto vc2019x64
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat" goto vc2017x64
if exist "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" goto vc2015x64
goto :done

:vc2022x64
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
goto :done

:vc2019x64
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
goto :done

:vc2017x64
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
goto :done

:vc2015x64
call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" amd64
goto :done

:done
endlocal
