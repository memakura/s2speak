# s2speech
Scratch 2 OpenJTalk (Speech Synthesis)    

## 必要なもの / Requirement
- Windows 10 (7? 8?)
- Scratch 2.0 (offline version)
- Python 3.5
    - pyaudio (pip install pyaudio)
    - aiohttp (pip install aiohttp)

## デモ
1. Scratch 2.0 (offline) を立ち上げる
1. scratch/project.sb2 を開く
1. Pythonの動くコマンドラインで s2speech.py を実行する : `python s2speech.py`

## 使い方
1. Scratch 2.0 を立ち上げる
1. [ファイル] をシフトクリックして実験的なHTTP拡張を読み込みを選ぶ
1. scratch/s2speech_JP.s2e を開く
1. s2speech.py を実行する

## 声の追加や変更 (htsvoices)
1. 追加の .hts ファイルもしくはフォルダを htsvoices/ に置く
1. htsvoices/voices.cfg を適当に編集する
1. 必要に応じて scratch/s2speech_JP.s2e を編集する (voice_id の番号追加など)
1. s2speech.py を実行する

----

## Demo
1. Run scratch 2.0 (offline)
1. Open scratch/project.sb2
1. Run s2speech.py from command line : `python s2speech.py`

## How to use
1. Run scratch 2.0
1. Shift-click the File menu and select "Import Experimental Extension"
1. Open scratch/s2speech.s2e
1. Run s2speech.py

## Add/change htsvoices
1. Add additional .hts files to htsvoices/
1. Edit htsvoices/voices.cfg
1. Edit scratch/speech.s2e if necessary (e.g., add numbers for voice_id)
1. Run s2speech.py

----
## Reference: https://github.com/nvdajp/python-jtalk/
- Updated scripts for Python 3.5
- jtalk directory is from nvdajp
- Compiled Mecab and OpenJTalk with 64bit

## Features
- Asynchronous I/O (asyncio) HTTP server (aiohttp)
- Config file for htsvoices : voices can be added easily
