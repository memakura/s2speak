# s2speech.py
# -*- coding: utf-8 -*-
# Scratch 2 Speech
#  2017.6
#  Hiroaki Kawashima

# --- Originally jtalkRunner.py ---
# Japanese speech engine test module
# by Takuya Nishimoto
# http://ja.nishimotz.com/project:libopenjtalk
# Usage:
# > python jtalkRunner.py
# requires pyaudio (PortAudio wrapper)
# http://people.csail.mit.edu/hubert/pyaudio/


import os
import sys
import wave
import time
import cProfile
import pstats
from jtalkCore import *
import jtalkPrepare

import configparser
import asyncio
from aiohttp import web


class s2jtalk:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 50210

        self.waiting_commands = set() # waiting block in scratch

        self.MECAB_DIR = r'.\jtalk'
        self.JT_LIB_DIR = r'.\jtalk'
        self.HTSVOICES_DIR = r'.\htsvoices'
        self.JT_DLL = os.path.join(self.JT_LIB_DIR, 'libopenjtalk.dll')

        config = configparser.ConfigParser()
        config.read(os.path.join(self.HTSVOICES_DIR, 'voices.cfg'))

        self.voices = [{'name':'zero'}] # dummy for index 0
        #for section in config.sections(): config[section]['name'] = section # add 'name' option
        #self.voices.extend([config[section] for section in config.sections()]) # list of dic
        for section in config.sections():
            v = config[section]
            self.voices.append({
                'name' : section,
                'lang' : v['lang'],
                'samp_rate' : int(v['samp_rate']),
                'fperiod' : int(v['fperiod']),
                'lf0_base' : float(v['lf0_base']),
                'pitch_bias' : float(v['pitch_bias']),
                'speaker_attenuation' : float(v['speaker_attenuation']),
                'htsvoice' : os.path.join(self.HTSVOICES_DIR, v['htsvoice'])
            })

        self.voice_id_max = len(self.voices)-1

        # default voice id
        self.voice_id = 1


    def pa_play(self, data, samp_rate=16000):
        import pyaudio
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(2), channels=1, rate=samp_rate, output=True)
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


    def do_synthesis(self, msg, voice_args, do_play, do_write, do_write_jt, do_log,
                     fperiod, pitch=50, inflection=50, vol=50):
        msg = jtalkPrepare.convert(msg)
        s = text2mecab(msg)
        print("utf-8: (%s)" % s.decode('utf-8', 'ignore'))
        mf = MecabFeatures()
        Mecab_analysis(s, mf)
        Mecab_print(mf, print)
        Mecab_correctFeatures(mf)
        ar = Mecab_splitFeatures(mf)
        print('array size %d' % len(ar))
        max_level = int(326.67 * int(vol) + 100) # 100..32767
        level = int(max_level * voice_args['speaker_attenuation'])
        lf0_amp = 0.020 * inflection # 50 = original range
        ls = 0.015 * (pitch - 50.0 + voice_args['pitch_bias']) # 50 = no shift
        lf0_offset = ls + voice_args['lf0_base'] * (1 - lf0_amp)
        count = 0
        for a in ar:
            count += 1
            print('feature size %d' % a.size)
            Mecab_print(a, print)
            Mecab_utf8_to_cp932(a)
            if do_write_jt:
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
                                   level_=level,
                                   fperiod_=fperiod,
                                   lf0_offset_=lf0_offset,
                                   lf0_amp_=lf0_amp,
                                   logwrite_=print,
                                   jtlogfile_=l,
                                   jtwavfile_=w)
            if data:
                print('data size %d' % len(data))
                if do_play:
                    self.pa_play(data, samp_rate=voice_args['samp_rate'])
                if do_write:
                    w = wave.Wave_write("_test%d.wav" % count)
                    w.setparams((1, 2, voice_args['samp_rate'],
                                 len(data)//2, 'NONE', 'not compressed'))
                    w.writeframes(data)
                    w.close()
            libjt_refresh()
            del a
        del mf

    async def _do_synthesis(self, s):
        v = self.voices[self.voice_id]
        self.do_synthesis(s + "。", v, do_play=True, do_write=False, do_write_jt=False, do_log=False,
                          fperiod=v['fperiod'], pitch=50, inflection=50)

    async def changevoice(self, request):
        self.voice_id = int(request.match_info['voice_id'])
        if self.voice_id > self.voice_id_max: self.voice_id = self.voice_id_max
        if self.voice_id < 1: self.voice_id = 1
        v = self.voices[self.voice_id]
        libjt_load(v['htsvoice'])
        print('changevoice: ', self.voice_id)
        return web.Response(text='ok')

    async def speak(self, request):
        s = request.match_info['utterance']
        print('speak: ', s)
        await self._do_synthesis(s)
        return web.Response(text='ok')

    async def speakwait(self, request):
        command_id = request.match_info['command_id']
        s = request.match_info['utterance']
        print('speakwait: ', s)
        self.waiting_commands.add(command_id)
        await self._do_synthesis(s)
        self.waiting_commands.remove(command_id)
        return web.Response(text='ok')

    async def poll(self, request):
        text = '_busy'
        for i in self.waiting_commands:
            text += ' ' + str(i)
        #if len(text) > 5: print(text)
        return web.Response(text=text)

    async def crossdomain(self, request):
        text = '<cross-domain-policy>'
        text += '<allow-access-from domain="*" to-ports="' + self.port + '"/>'
        text += '</cross-domain-policy>'
        return web.Response(text=text)

    def main(self):
        njd = NJD()
        jpcommon = JPCommon()
        engine = HTS_Engine()
        libjt_initialize(self.JT_DLL)
        v = self.voices[self.voice_id]
        libjt_load(v['htsvoice'])
        Mecab_initialize(print, self.MECAB_DIR)

        app = web.Application()
        app.router.add_get('/changevoice/{voice_id}', self.changevoice)
        app.router.add_get('/speak/{utterance}', self.speak)
        app.router.add_get('/speakwait/{command_id}/{utterance}', self.speakwait)
        app.router.add_get('/poll', self.poll)
        app.router.add_get('/crossdomain.xml', self.crossdomain)
        web.run_app(app, host=self.host, port=self.port)


if __name__ == '__main__':
    server = s2jtalk()
    server.main()
