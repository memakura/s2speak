#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 s2speech.py
 Scratch 2 Speech
  2017.6
  Hiroaki Kawashima
 --- Special thanks to jtalkRunner.py ---
 Japanese speech engine test module
 by Takuya Nishimoto
 http://ja.nishimotz.com/project:libopenjtalk
"""

import os
import sys
import wave
import time
import cProfile
import pstats
from jtalkCore import *
import jtalkPrepare

import urllib
import asyncio
from aiohttp import web


class S2JTalk:
    """ scratch 2 openjtalk """
    def __init__(self):
        self.helper_host = '127.0.0.1'
        self.helper_port = 50210 # port of this helper

        self.waiting_commands = set() # waiting block in scratch
        self.speaking = False
        self.volume = 50 # default volume

        self.mecab_dir = r'.\jtalk'
        self.jt_lib_dir = r'.\jtalk'
        self.htsvoices_dir = r'.\htsvoices'
        self.jt_dll = os.path.join(self.jt_lib_dir, 'libopenjtalk.dll')

        # create a folder for user-prepared htsvoices if not exists
        self.user_htsvoices_dir = os.path.join(os.getenv('LOCALAPPDATA'), r's2speech\htsvoices')
        print(self.user_htsvoices_dir)
        if not os.path.exists(self.user_htsvoices_dir):
            os.makedirs(self.user_htsvoices_dir)

        def _readconfig(path):
            """ prepare voice settings """
            import configparser
            config = configparser.ConfigParser()
            config.read(path)
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
                    'htsvoice' : os.path.join(self.htsvoices_dir, v['htsvoice'])
                })

        self.voices = [{'name':'zero'}] # dummy for index 0
        for dir_path in [self.htsvoices_dir, self.user_htsvoices_dir]:
            cfgfile_path = os.path.join(dir_path, 'voices.cfg')
            if os.path.isfile(cfgfile_path):
                _readconfig(cfgfile_path)

        self.voice_id_max = len(self.voices)-1
        # print loaded voices
        for i in range(1, len(self.voices)):
            print(i, ':', self.voices[i]['name'])

        # default voice id
        self.voice_id = 1


    # todo: async (need exclusive access)
    async def pa_play(self, data, samp_rate=16000):
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
        #time.sleep(float(size) / 2 / samp_rate)
        await asyncio.sleep(float(size) / 2 / samp_rate)
        stream.close()
        p.terminate()


    async def _do_synthesis(self, msg, voice_args): #, future):
        do_play = True
        do_write = False
        do_write_jt = False
        do_log = False
        fperiod = voice_args['fperiod']
        pitch = 50
        inflection = 50
        vol = self.volume
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
                    await self.pa_play(data, samp_rate=voice_args['samp_rate'])
                if do_write:
                    w = wave.Wave_write("_test%d.wav" % count)
                    w.setparams((1, 2, voice_args['samp_rate'],
                                 len(data)//2, 'NONE', 'not compressed'))
                    w.writeframes(data)
                    w.close()
            libjt_refresh()
            del a
        del mf
        #future.set_result(0)

    async def do_synthesis(self, s):
        """ call libjt exclusively """
        #loop = asyncio.get_event_loop()
        #future = loop.create_future()
        v = self.voices[self.voice_id]
        while self.speaking: # wait for complesion of previous speech
            await asyncio.sleep(0.01)
        self.speaking = True # libjt should be called exlusively
        await self._do_synthesis(s + "。", v)
        self.speaking = False
        #loop.call_soon(self._do_synthesis, s + "。", v, future)
        #return await future

    async def speak(self, request):
        s = request.match_info['utterance']
        print('speak: ', s)
        await self.do_synthesis(s)
        return web.Response(text='ok')

    async def speakwait(self, request):
        command_id = request.match_info['command_id']
        self.waiting_commands.add(command_id)
        s = request.match_info['utterance']
        print('speakwait: ', s)
        await self.do_synthesis(s)
        self.waiting_commands.remove(command_id)
        return web.Response(text='ok')

    async def changevoice(self, request):
        try:
            val = int(request.match_info['voice_id']) # need errorcheck here
        except ValueError:
            print("Ignored. Not a number: ", request.match_info['voice_id'])
            return web.Response(text='failed')
        command_id = request.match_info['command_id']
        self.waiting_commands.add(command_id)
        if val > self.voice_id_max: self.voice_id = self.voice_id_max
        elif val < 1: self.voice_id = 1
        else: self.voice_id = val
        print("changevoice: ", str(self.voice_id))
        v = self.voices[self.voice_id]
        libjt_load(v['htsvoice'])
        self.waiting_commands.remove(command_id)
        return web.Response(text='ok')

    async def changevolume(self, request):
        try:
            val = int(request.match_info['volume']) # need errorcheck here
        except ValueError:
            print("Ignored. Not a number: ", request.match_info['volume'])
            return web.Response(text='failed')
        command_id = request.match_info['command_id']
        self.waiting_commands.add(command_id)
        if val > 100: self.volume = 100
        elif val < 0: self.volume = 0
        else: self.volume = val
        print("changevolume: ", str(self.volume))
        self.waiting_commands.remove(command_id)
        return web.Response(text='ok')

    async def poll(self, request):
        text = ''
        text += 'voicename ' + urllib.parse.quote(self.voices[self.voice_id]['name']) + '\n'
        text += 'volume ' + str(self.volume) + '\n'
        text += '_busy '
        text += ' '.join(self.waiting_commands)
        #print(text)
        return web.Response(text=text)

    async def crossdomain(self, request):
        text = '<cross-domain-policy>'
        text += '<allow-access-from domain="*" to-ports="' + str(self.helper_port) + '"/>'
        text += '</cross-domain-policy>'
        return web.Response(text=text)

    def main(self):
        njd = NJD()
        jpcommon = JPCommon()
        engine = HTS_Engine()
        libjt_initialize(self.jt_dll)
        v = self.voices[self.voice_id]
        libjt_load(v['htsvoice'])
        Mecab_initialize(print, self.mecab_dir)

        app = web.Application()
        app.router.add_get('/speak/{utterance}', self.speak)
        app.router.add_get('/speakwait/{command_id}/{utterance}', self.speakwait)
        app.router.add_get('/changevoice/{command_id}/{voice_id}', self.changevoice)
        app.router.add_get('/changevolume/{command_id}/{volume}', self.changevolume)
        app.router.add_get('/poll', self.poll)
        app.router.add_get('/crossdomain.xml', self.crossdomain)
        #try:
        web.run_app(app, host=self.helper_host, port=self.helper_port)
        #finally:
        #    web.close()

if __name__ == '__main__':
    s2jtalk = S2JTalk()
    s2jtalk.main()
