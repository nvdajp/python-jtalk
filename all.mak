!IF "$(MACHINE)" == ""
MACHINE=x86
!ENDIF

all:
	nmake /f hts.mak MACHINE=$(MACHINE)
	cd libopenjtalk
	cd text2mecab
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	rem cd mecab
	rem nmake /f Makefile.mak
	rem cd ..
	cd mecab2njd
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd njd
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd njd_set_pronunciation
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd njd_set_digit
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd njd_set_accent_phrase
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd njd_set_accent_type
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd njd_set_unvoiced_vowel
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd njd_set_long_vowel
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd njd2jpcommon
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd ..
	cd jpcommon
	copy ..\libopenjtalk\jpcommon\*.c .
	copy ..\libopenjtalk\jpcommon\*.h .
	copy ..\libopenjtalk\jpcommon\Makefile.mak .
	patch jpcommon_label.c jpcommon_label.patch
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
	cd lib
	nmake /f Makefile.mak MACHINE=$(MACHINE)
	cd ..
!IF "$(MACHINE)" == "x64"
	if not exist x64 mkdir x64
	copy /Y lib\libopenjtalk.dll x64\libopenjtalk.dll
!ELSE
	copy /Y lib\libopenjtalk.dll .
!ENDIF

clean_all:
	nmake /f hts.mak clean MACHINE=$(MACHINE)
	cd libopenjtalk
	cd text2mecab
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd mecab
	nmake /f Makefile.mak clean
	cd ..
	cd mecab2njd
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd njd
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd njd_set_pronunciation
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd njd_set_digit
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd njd_set_accent_phrase
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd njd_set_accent_type
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd njd_set_unvoiced_vowel
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd njd_set_long_vowel
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd njd2jpcommon
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..
	cd ..
	cd jpcommon
	del /Q *.c *.h *.orig *.obj *.lib *.mak 2>nul
	cd ..
	cd lib
	nmake /f Makefile.mak clean MACHINE=$(MACHINE)
	cd ..

clean: clean_all
