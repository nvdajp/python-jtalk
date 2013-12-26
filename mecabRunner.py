# mecabRunner.py 
# -*- coding: utf-8 -*-
# Japanese text processor test module
# by Takuya Nishimoto

from __future__ import unicode_literals
import os
import sys
from mecab import *
from mecabHarness import tasks

def __print(s):
	print s.encode('utf-8', 'ignore')

buffer = ''

def __print_dummy(s):
	global buffer
	buffer += s + '\n'

def Mecab_get_reading(mf, CODE_=CODE):
	reading = ''
	braille = ''
	for pos in xrange(0, mf.size):
		ar = Mecab_getFeature(mf, pos, CODE_=CODE_).split(',')
		rd = ''
		if len(ar) > 9:
			rd = ar[9].replace('\u3000', ' ')
		elif ar[0] != 'ー':
			rd = ar[0]
		reading += rd
		if len(ar) > 12:
			braille += ar[12] + r"/"
		else:
			braille += rd + r"/"
	return (reading, braille.rstrip(r" /"))

def get_reading(msg):
	s = Mecab_text2mecab(msg)
	mf = MecabFeatures()
	Mecab_analysis(s, mf)
	Mecab_correctFeatures(mf)
	Mecab_print(mf, __print_dummy)
	reading = Mecab_get_reading(mf)
	mf = None
	return reading

if __name__ == '__main__':
	JT_DIR = '.'
	print JT_DIR
	Mecab_initialize(__print, JT_DIR)
	for i in tasks:
		if isinstance(i, dict):
			if 'braille' in i:
				if 'speech' in i:
					item = [ i['text'], i['speech'], i['braille'] ]
				else:
					s = i['braille'].replace(' ', '').replace('/', '')
					item = [ i['text'], s, i['braille'] ]
			elif 'input' in i:
				if 'speech' in i:
					item = [ i['text'], i['speech'], i['input'] ]
				else:
					s = i['input'].replace(' ', '').replace('/', '')
					item = [ i['text'], s, i['input'] ]
			else:
				item = [ i['text'], i['speech'] ]
		else:
			item = i
		buffer = ''
		result = get_reading(item[0])
		if item[1] is not None and result[0] != item[1]:
			__print('')
			__print('')
			__print(buffer)
			__print('input:    ' + item[0])
			__print('reading expected: ' + item[1])
			__print('reading result:   ' + result[0])
		if len(item) > 2 and result[1] != item[2]:
			__print('')
			__print('')
			__print(buffer)
			__print('input:            ' + item[0])
			__print('braille expected: ' + item[2])
			__print('braille result:   ' + result[1])

	
