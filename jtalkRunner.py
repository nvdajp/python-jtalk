# jtalkRunner.py
# -*- coding: utf-8 -*-
# Japanese speech engine test module
# by Takuya Nishimoto
# http://ja.nishimotz.com/project:libopenjtalk
# Usage:
# > cd source
# > python synthDrivers/jtalk/_jtalk_runner.py
# requires pyaudio (PortAudio wrapper)
# http://people.csail.mit.edu/hubert/pyaudio/

from __future__ import unicode_literals, print_function
import os
import sys
import wave
import time
import pyaudio
import cProfile
import pstats
from jtalk_core import *
import nvdajp_predic 

JT_DIR = r'.'
JT_LIB_DIR = r'.'
JT_DLL = os.path.join(JT_LIB_DIR, 'libopenjtalk.dll')

voices = [
	{
		"id": "V1",
		"name": "m001",
		"lang":"ja",
		"samp_rate": 48000,
		"fperiod": 240,
		"lf0_base":5.0,
		"speaker_attenuation":1.0,
		"htsvoice": os.path.join(JT_DIR, 'm001', 'm001.htsvoice')
		},
	]

def pa_play(data, samp_rate = 16000):
	p = pyaudio.PyAudio()
	stream = p.open(format = p.get_format_from_width(2),
		channels = 1, rate = samp_rate, output = True)
	size = len(data)
	pos = 0 # byte count
	while pos < size:
		a = stream.get_write_available() * 2
		o = data[pos:pos+a]
		stream.write(o)
		pos += a
	time.sleep(float(size) / 2 / samp_rate)
	stream.close()
	p.terminate()

def __print(s):
	print(s.encode('cp932', 'ignore'))

def print_code(msg):
	s = ''
	for c in msg:
		s += '%04x ' % ord(c)
	print(s)

def do_synthesis(msg, voice_args, do_play, do_write, do_log):
	msg = nvdajp_predic.convert(msg)
	s = Mecab_text2mecab(msg, CODE_='utf-8')
	__print("utf-8: (%s)" % s.decode('utf-8', 'ignore'))
	mf = MecabFeatures()
	Mecab_analysis(s, mf)
	Mecab_print(mf, __print, CODE_='utf-8')
	Mecab_correctFeatures(mf, CODE_='utf-8')
	fperiod = voice_args['fperiod']
	ar = Mecab_splitFeatures(mf, CODE_='utf-8')
	__print('array size %d' % len(ar))
	count = 0
	for a in ar:
		count += 1
		__print('feature size %d' % a.size)
		Mecab_print(a, __print, CODE_='utf-8')
		Mecab_utf8_to_cp932(a)
		if do_write:
			w = "_test%d.jt.wav" % count
		else:
			w = None
		if do_log:
			l = "_test%d.jtlog" % count
		else:
			l = None
		data = libjt_synthesis(a.feature,
							   a.size,
							   begin_thres_=32,
							   end_thres_=32,
							   fperiod_ = fperiod,
							   logwrite_ = __print,
							   jtlogfile_ = l,
							   jtwavfile_ = w)
		if data:
			__print('data size %d' % len(data))
			if do_play:
				pa_play(data, samp_rate = voice_args['samp_rate'])
			if do_write:
				w = wave.Wave_write("_test%d.wav" % count)
				w.setparams( (1, 2, voice_args['samp_rate'], len(data)/2,
							  'NONE', 'not compressed') )
				w.writeframes(data)
				w.close()
		libjt_refresh()
		del a
	del mf

def main(do_play = False, do_write = True, do_log = False):
	njd = NJD()
	jpcommon = JPCommon()
	engine = HTS_Engine()
	libjt_initialize(JT_DLL)
	v = voices[0]
	libjt_load(v['htsvoice'])
	Mecab_initialize(__print, JT_DIR)
	nvdajp_predic.setup()

	msgs = [
		'100.25ドル。ウェルカムトゥー nvda テンキーのinsertキーと、メインのinsertキーの両方が、nvdaキーとして動作します',
		'マーク。まーく。',
		]
	s = msgs[0]
	print(len(s))
	do_synthesis(s, v, do_play, do_write, do_log)

if __name__ == '__main__':
	main(do_play=False, do_write=True)
	#prof = cProfile.run("main(do_play=True)", '_cprof.prof')
	#p = pstats.Stats('_cprof.prof')
	#p.strip_dirs()
	#p.sort_stats('time', 'calls')
	#p.print_stats()
