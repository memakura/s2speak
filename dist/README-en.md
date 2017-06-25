# s2speech Installer
Use OpenJTalk from scratch 2 offline editor

![s2speech](https://github.com/memakura/s2speech/blob/master/images/ScratchSpeechSynth.png)
![block_and_sample](https://github.com/memakura/s2speech/blob/master/images/block_and_sample.png)

## Installation
1. Select [Download] from https://github.com/memakura/s2speech/blob/master/dist/s2speech-0.2-amd64.msi
    1. msi and files to be installed are large（more than 100MB files will be installed）
1. Run the downloaded msi file
    1. You may see warning messages if using Windows 7, 8, or 10
1. In what follows, "C:\Program Files\s2speech" is assumed to be the installed folder

## Run s2speech
- Start s2speech by clicking the shortcut on the desktop and check if "==== Running on http://127.0.0.1:50210 ====" appears
    1. "voice_id : name_of_voice" in voices.cfg will be displayed
    1. In the "More blocks" section of scratch editor, the red circle becomes green if s2speech correctly started

## How to use
- The following demo is helful to understand the blocks
    - "C:\Program Files\s2speech\00scratch/project.sb2"
- How to create a new project
    1. In the Scratch2 offline editor, shift-click the File menu and select "Import Experimental Extension"
    1. Select and open "C:\Program Files\s2speech\00scratch\s2speech.s2e" (This file can be copied to other folder for editing)

## Add/change htsvoices
1. Add additional .hts files and/or folders "C:\Users\<username>\AppData\Local\s2speech\htsvoices", and create "voices.cfg" to the same folder
    - The htsvoices folder will be created automatically when you run s2speech for the first time
    - "C:\Program Files\s2speech\htsvoices" is a good reference to know how to locate hts files/folders and create voices.cfg
    - User htsvoices will be loaded after "C:\Program Files\s2speech\htsvoices" is loaded (voice_id numbers follow after the original voices)
    1. Copy and edit 00scratch/speech.s2e if necessary (e.g., add numbers for voice_id)
1. Run s2speech.py

## Notes
- Original python-jtalk scripts are from https://github.com/nvdajp/python-jtalk/
    - Some scripts were updated for Python 3.5 and 64bit compiling
- jtalk directory is from nvdajp
- Mecab and OpenJTalk DLLs were compiled with 64bit
