# jtalkRunner.py
# -*- coding: utf-8 -*-
# Japanese speech engine test module
# by Takuya Nishimoto
# http://ja.nishimotz.com/project:libopenjtalk
# Usage:
# > python jtalkRunner.py
# requires pyaudio (PortAudio wrapper)
# http://people.csail.mit.edu/hubert/pyaudio/

from __future__ import unicode_literals, print_function
import os
import sys
import wave
import time
import cProfile
import pstats
from jtalkCore import *
import jtalkPrepare

JT_DIR = r"..\nvdajp\source\synthDrivers\jtalk"
JT_LIB_DIR = r"."
JT_DLL = os.path.join(JT_LIB_DIR, "libopenjtalk.dll")

voices = [
    {
        "id": "V1",
        "name": "m1",
        "lang": "ja",
        "samp_rate": 48000,
        "fperiod": 240,
        "lf0_base": 5.0,
        "speaker_attenuation": 1.0,
        "htsvoice": os.path.join(JT_DIR, "m001", "m001.htsvoice"),
        # "espeak_variant": "max",
    },
    {
        "id": "V2",
        "name": "mei",
        "lang": "ja",
        "samp_rate": 48000,
        "fperiod": 240,
        "lf0_base": 5.86,
        "pitch_bias": -10,
        "speaker_attenuation": 0.5,
        "htsvoice": os.path.join(JT_DIR, "mei", "mei_normal.htsvoice"),
        # "espeak_variant": "f1",
    },
    {
        "id": "V3",
        "name": "lite",
        "lang": "ja",
        "samp_rate": 16000,
        "fperiod": 80,
        "lf0_base": 5.0,
        "pitch_bias": 0,
        "speaker_attenuation": 1.0,
        "htsvoice": os.path.join(JT_DIR, "lite", "voice.htsvoice"),
        # "espeak_variant": "max",
    },
]


def pa_play(data, samp_rate=16000):
    import pyaudio

    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(2), channels=1, rate=samp_rate, output=True
    )
    size = len(data)
    pos = 0  # byte count
    while pos < size:
        a = stream.get_write_available() * 2
        o = data[pos : pos + a]
        stream.write(o)
        pos += a
    time.sleep(float(size) / 2 / samp_rate)
    stream.close()
    p.terminate()


def __print(s):
    print(s.encode("cp932", "ignore"))


def print_code(msg):
    s = ""
    for c in msg:
        s += "%04x " % ord(c)
    print(s)


def do_synthesis(
    msg,
    voice_args,
    do_play,
    do_write,
    do_write_jt,
    do_log,
    fperiod,
    pitch=50,
    inflection=50,
    vol=50,
):
    msg = jtalkPrepare.convert(msg)
    s = text2mecab(msg)
    __print("utf-8: (%s)" % s.decode("utf-8", "ignore"))
    mf = MecabFeatures()
    Mecab_analysis(s, mf)
    Mecab_print(mf, __print)
    Mecab_correctFeatures(mf)
    ar = Mecab_splitFeatures(mf)
    __print("array size %d" % len(ar))
    max_level = int(326.67 * int(vol) + 100)  # 100..32767
    level = int(max_level * voice_args["speaker_attenuation"])
    lf0_amp = 0.020 * inflection  # 50 = original range
    ls = 0.015 * (pitch - 50.0 + voice_args["pitch_bias"])  # 50 = no shift
    lf0_offset = ls + voice_args["lf0_base"] * (1 - lf0_amp)
    count = 0
    for a in ar:
        count += 1
        __print("feature size %d" % a.size)
        Mecab_print(a, __print)
        Mecab_utf8_to_cp932(a)
        if do_write_jt:
            w = "_test%d.jt.wav" % count
        else:
            w = None
        if do_log:
            l = "_test%d.jtlog" % count
        else:
            l = None
        data = libjt_synthesis(
            a.feature,
            a.size,
            begin_thres_=32,
            end_thres_=32,
            level_=level,
            fperiod_=fperiod,
            lf0_offset_=lf0_offset,
            lf0_amp_=lf0_amp,
            logwrite_=__print,
            jtlogfile_=l,
            jtwavfile_=w,
        )
        if data:
            __print("data size %d" % len(data))
            if do_play:
                pa_play(data, samp_rate=voice_args["samp_rate"])
            if do_write:
                w = wave.Wave_write("_test%d.wav" % count)
                w.setparams(
                    (
                        1,
                        2,
                        voice_args["samp_rate"],
                        len(data) / 2,
                        "NONE",
                        "not compressed",
                    )
                )
                w.writeframes(data)
                w.close()
        libjt_refresh()
        del a
    del mf


def main(
    do_play=False, do_write=True, do_write_jt=False, do_log=False, voice_id=1, s=""
):
    njd = NJD()
    jpcommon = JPCommon()
    engine = HTS_Engine()
    libjt_initialize(JT_DLL)
    v = voices[voice_id]
    libjt_load(v["htsvoice"])
    Mecab_initialize(__print, JT_DIR)
    fperiod = v["fperiod"]
    do_synthesis(
        s, v, do_play, do_write, do_write_jt, do_log, fperiod, pitch=50, inflection=50
    )


if __name__ == "__main__":
    main(do_play=False, do_write=True, do_log=True, voice_id=1, s="100.25ドル")
    # prof = cProfile.run("main(do_play=True)", '_cprof.prof')
    # p = pstats.Stats('_cprof.prof')
    # p.strip_dirs()
    # p.sort_stats('time', 'calls')
    # p.print_stats()
