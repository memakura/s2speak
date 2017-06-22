# s2speech
Scratch 2 Speech (wrapping python-openjtalk)

![s2speech](https://github.com/memakura/s2speech/blob/master/images/ScratchSpeechSynth.png)

## 必要なもの / Requirement
- Windows 10 (64bit) (Windows 7 や 8でも可?)
- Scratch 2 offline editor
- **dist 以下のインストーラを用いる場合は Python不要**
    - ![Installer](https://github.com/memakura/s2speech/blog/master/dist/s2speech-0.1-amd64.msi)
- Python 3.5 (64bit) (pythonで直接実行する場合)
    - pyaudio (pip install pyaudio しておく)
    - aiohttp (pip install aiohttp しておく)

## デモ
1. Scratch 2 (offline) を立ち上げる
1. 00scratch/project.sb2 を開く
1. Pythonの動くコマンドラインで s2speech.py を実行する : `python s2speech.py`

## 使い方
1. Scratch 2 を立ち上げる
1. [ファイル] をシフトクリックして実験的なHTTP拡張を読み込みを選ぶ
1. 00scratch/s2speech_JP.s2e を開く
1. s2speech.py を実行する

## 声の追加や変更 (htsvoices)
1. 追加の .hts ファイルもしくはフォルダを htsvoices/ に置く
1. htsvoices/voices.cfg を適当に編集する
1. 必要に応じて scratch/s2speech_JP.s2e を編集する (voice_id の番号追加など)
1. s2speech.py を実行する

----

## Demo
1. Run scratch 2 (offline)
1. Open 00scratch/project.sb2
1. Run s2speech.py from command line : `python s2speech.py`

## How to use
1. Run scratch 2
1. Shift-click the File menu and select "Import Experimental Extension"
1. Open 00scratch/s2speech.s2e
1. Run s2speech.py

## Add/change htsvoices
1. Add additional .hts files to htsvoices/
1. Edit htsvoices/voices.cfg
1. Edit scratch/speech.s2e if necessary (e.g., add numbers for voice_id)
1. Run s2speech.py

----
## Notes
- Original python-jtalk scripts are from https://github.com/nvdajp/python-jtalk/
    - Some scripts were updated for Python 3.5 and 64bit compiling
- jtalk directory is from nvdajp
- Mecab and OpenJTalk DLLs were compiled with 64bit
- Asynchronous I/O (asyncio) HTTP server (aiohttp) is used
- To build .msi, run `python setup.py bdist_msi` with python 3.5 (64bit)

## License
- GPL 3.0

