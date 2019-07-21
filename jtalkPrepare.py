# nvdajp_predic.py
# -*- coding: utf-8 -*-
# for python-jtalk

import re
import sys
if sys.version_info.major >= 3:
	re_ascii = re.ASCII
else:
	re_ascii = 0

predic = None

def setup():
	global predic
	if predic is None:
		predic = load()

def convert(msg):
	setup()
	for p in predic:
		try:
			msg = re.sub(p[0], p[1], msg)
		except:
			pass
	msg = msg.lower()
	return msg

def load():
	return [
		[re.compile(u'^ー$'), u'チョーオン'],
		[re.compile(u'^ン$'), u'ウン'],
		[re.compile(u'\\sー$'), u' チョーオン'],
		[re.compile(u'\\sン$'), u' ウン'],

		## 人々 昔々 家々 山々 
 		[re.compile(u'(.)々'), u'\\1\\1'],

		## isolated hiragana HA (mecab replaces to WA)
		## は 
		[re.compile(u'^は$'), u'ハ'],
		[re.compile(u'\\sは$'), u' ハ'],
		
		## 59 名
		[re.compile(u'(\\d) 名'), u'\\1名'],
		## 4行 ヨンコー -> ヨンギョー
		[re.compile(u'(\\d)行'), u'\\1ギョー'],
		## 2 分前更新
		[re.compile(u'(\\d)+ 分前更新'), u'\\1分マエコーシン'],
		
		## 1MB 10MB 1.2MB 0.5MB 321.0MB 123.45MB 2.7GB
		## 1 MB 10 MB 1.2 MB 0.5 MB 321.0 MB 123.45 MB 2.7 GB
		[re.compile(u'(\\d+)\\s*KB'), u'\\1キロバイト'],
		[re.compile(u'(\\d+)\\s*MB'), u'\\1メガバイト'],
		[re.compile(u'(\\d+)\\s*GB'), u'\\1ギガバイト'],
		[re.compile(u'(\\d+)\\s*MHz'), u'\\1メガヘルツ'],
		[re.compile(u'(\\d+)\\s*GHz'), u'\\1ギガヘルツ'],

		## 2013 年 1 月 2 日
		[re.compile(u'(\\d+)\\s+年\\s+(\\d+)\\s+月\\s+(\\d+)\\s+日'), u'\\1年\\2月\\3日'],

		### zenkaku symbols convert
		## ２０１１．０３．１１
		## １，２３４円
		[re.compile(u'．'), u'.'],
		[re.compile(u'，'), u','],

		## 1,234
		## 1,234,567
		## 1,234,567,890
		## 1,23 = ichi comma niju san
		## 1,0 = ichi comma zero
		[re.compile(u'(\\d)\\,(\\d{3})'), u'\\1\\2'],
		[re.compile(u'(\\d{2})\\,(\\d{3})'), u'\\1\\2'],
		[re.compile(u'(\\d{3})\\,(\\d{3})'), u'\\1\\2'],
		[re.compile(u'(\\d)\\,(\\d{1,2})'), u'\\1カンマ\\2'],

		[re.compile(u'(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})'), u'\\1テン\\2テン\\3テン\\4'],
		[re.compile(u'(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})'), u'\\1テン\\2テン\\3'],

		# do not replace '0' after '.' to phonetic symbols (prepare)
		[re.compile(u'\\.0'), u'.0\u00a0'],

		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)', re_ascii), u'  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5  \u00a0\\6  \u00a0\\7  \u00a0\\8  \u00a0\\9 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)', re_ascii), u'  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5  \u00a0\\6  \u00a0\\7  \u00a0\\8 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)', re_ascii), u'  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5  \u00a0\\6  \u00a0\\7 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)', re_ascii), u'  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5  \u00a0\\6 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)', re_ascii), u'  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)', re_ascii), u'  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)', re_ascii), u'  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3 '],
		[re.compile(u'\\b0(\\d)(\\d)', re_ascii), u'  \u00a00  \u00a0\\1  \u00a0\\2 '],
		[re.compile(u'\\b0(\\d)', re_ascii), u'  \u00a00  \u00a0\\1 '],

		[re.compile(u' \u00a00'), u'ゼロ'],
		[re.compile(u' \u00a01'), u'イチ'],
		[re.compile(u' \u00a02'), u'ニー'],
		[re.compile(u' \u00a03'), u'サン'],
		[re.compile(u' \u00a04'), u'ヨン'],
		[re.compile(u' \u00a05'), u'ゴー'],
		[re.compile(u' \u00a06'), u'ロク'],
		[re.compile(u' \u00a07'), u'ナナ'],
		[re.compile(u' \u00a08'), u'ハチ'],
		[re.compile(u' \u00a09'), u'キュー'],

		# do not replace '0' after '.' to phonetic symbols (finalize)
		[re.compile(u'\\.0\u00a0'), u'.0'],
	]

