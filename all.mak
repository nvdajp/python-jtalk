all:
	nmake /f hts.mak
	cd libopenjtalk
	cd text2mecab
	nmake /f Makefile.mak
	cd ..
	rem cd mecab
	rem nmake /f Makefile.mak
	rem cd ..
	cd mecab2njd
	nmake /f Makefile.mak
	cd ..
	cd njd
	nmake /f Makefile.mak
	cd ..
	cd njd_set_pronunciation
	nmake /f Makefile.mak
	cd ..
	cd njd_set_digit
	nmake /f Makefile.mak
	cd ..
	cd njd_set_accent_phrase
	nmake /f Makefile.mak
	cd ..
	cd njd_set_accent_type
	nmake /f Makefile.mak
	cd ..
	cd njd_set_unvoiced_vowel
	nmake /f Makefile.mak
	cd ..
	cd njd_set_long_vowel
	nmake /f Makefile.mak
	cd ..
	cd njd2jpcommon
	nmake /f Makefile.mak
	cd ..
	cd jpcommon
	nmake /f Makefile.mak
	cd ..
	cd ..
	cd lib
	nmake /f Makefile.mak
	cd ..
	copy lib\libopenjtalk.dll .

clean:
	nmake /f hts.mak clean
	cd libopenjtalk
	cd text2mecab
	nmake /f Makefile.mak clean
	cd ..
	cd mecab
	nmake /f Makefile.mak clean
	cd ..
	cd mecab2njd
	nmake /f Makefile.mak clean
	cd ..
	cd njd
	nmake /f Makefile.mak clean
	cd ..
	cd njd_set_pronunciation
	nmake /f Makefile.mak clean
	cd ..
	cd njd_set_digit
	nmake /f Makefile.mak clean
	cd ..
	cd njd_set_accent_phrase
	nmake /f Makefile.mak clean
	cd ..
	cd njd_set_accent_type
	nmake /f Makefile.mak clean
	cd ..
	cd njd_set_unvoiced_vowel
	nmake /f Makefile.mak clean
	cd ..
	cd njd_set_long_vowel
	nmake /f Makefile.mak clean
	cd ..
	cd njd2jpcommon
	nmake /f Makefile.mak clean
	cd ..
	cd jpcommon
	nmake /f Makefile.mak clean
	cd ..
	cd ..
	cd lib
	nmake /f Makefile.mak clean
	cd ..
