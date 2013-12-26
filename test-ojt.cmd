set DIC=dic
@rem set VOICE=m001\m001.htsvoice
@rem set VOICE=lite\voice.htsvoice
set VOICE=mei\mei_normal.htsvoice
set OUT=_out.wav
set LOG=_trace.txt
set EXE=c:\open_jtalk\bin\open_jtalk.exe
del /Q %OUT%
@rem %EXE% -h
echo "abc12345" | %EXE% -m %VOICE% -x %DIC% -ot %LOG% -ow %OUT%
start %OUT%
