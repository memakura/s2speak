# s2speech の使い方
scratch 2.0 (オフライン版) で音声合成ができます (OpenJTalk を使っています)．

![s2speech](https://github.com/memakura/s2speech/blob/master/images/ScratchSpeechSynth.png)
![block_and_sample](https://github.com/memakura/s2speech/blob/master/images/block_and_sample_JA.png)


## インストール方法
1. https://github.com/memakura/s2speech/blob/master/dist/s2speech-0.3-amd64.msi にて [Download] を選んでください．
    - msiファイルおよびインストールされるファイル一式はいずれもサイズが大きいので注意してください（100MB以上は必要）
1. ダウンロードされた msi ファイルを実行
    1. Windows8以上では「WindowsによってPCが保護されました」と出る場合があるので，[詳細情報] をクリックして [実行] してください．
    1. Windows7では「発行元が不明」と出るかもしれませんが，これも同じく[実行] を選んでください．
    1. （このほかウイルスチェックソフトでも発行元が不明に関して何かしら警告が出る可能性があります．）
1. インストール先は変えることができますが，特に指定しなければ "C:\Program Files\s2speech" にインストールされます．(以下ではここにインストールしたことを前提に説明します．)

## s2speechの起動方法
- デスクトップ上の s2speech を立ち上げて「==== Running on http://127.0.0.1:50210 ====」が表示されれば起動完了です．
    1. voices.cfg で登録されている「声の番号 : 声の名前」のリストが起動時に表示されます．
    1. 正しく起動されていれば，Scratch の「その他」ブロックの s2speechにて赤丸から緑丸になります．

## Scratchでのプロジェクトの作り方
- 以下のデモが参考になります．
    - "C:\Program Files\s2speech\00scratch/s2speech_demo.sb2"
- 新たに作成するとき
    1. Scratch2 offline editor でシフトキーを押しながら「ファイル」->「実験的なHTTP拡張を読み込み」を選んでください．
    1. "C:\Program Files\s2speech\00scratch\s2speech_JA.s2e" を選択してください．（このファイルはデスクトップなど，別の分かりやすい場所にコピーしておいてもよいです．)

## ブロックの説明
- [...]と話す: テキストボックスの中に書いた言葉を話します．話し終わるのを待たずに，次のブロックに進みます．しゃべりながら何か動かしたい場合などはこちらを使います．
- [...]と話す(終わるまで待つ): 話し終わるまでそのブロックで待ちます．
- 声を(...)にする: 声を変えます（どの番号でどんな声が出るかは試してみてください．番号と声の対応は今後変わる可能性があります）
- 話す音量を(...)にする: 声の大きさを変えます．0-100で指定してください．あまり大きくしないほうがよいです．
- 声の名前: 声には名前もついています．現在指定している声の名前が取り出せます．
- 話す音量: 現在指定している音量を取り出せます．

## 拡張機能：声の追加や変更 (htsvoices)
インターネット上には .hts 形式の声のファイルが公開されていたりします．ここでは声のファイルの追加方法を説明します．
1. 追加の .hts ファイルもしくはフォルダを "C:\Users\(ユーザ名)\AppData\Local\s2speech\htsvoices" に置き，同フォルダに voices.cfg を作成します．
    - 初めて実行したときに htsvoicesフォルダが自動作成されます．
    - htsファイルの置き方や voices.cfg の作成は "C:\Program Files\s2speech\htsvoices" を参考にしてください．
    - s2speech実行時に，"C:\Program Files\s2speech\htsvoices" に追加する形で htsファイルが読み込まれます． (voice_id の番号も追加されて順にふられます．)
1. 必要に応じて 00scratch\s2speech_JA.s2e をコピー・編集して使ってください．(voice_id の番号を追加する必要があります．)

## Notes
- nvdajp(https://github.com/nvdajp/nvdajp) というスクリーンリーダー(読み上げソフト)の開発コードの一部を使用しています．具体的には以下の通りです．
    - DLL を呼ぶための python-jtalk スクリプトは https://github.com/nvdajp/python-jtalk/ からです．
    - jtalk directory は nvdajp からのものです．
    - Mecab と OpenJTalk DLLs はもともと32bit版でしたが，64bit で別途コンパイルしました．
- nvdajp および OpenJTalk や Mecab，htsvoices などはそれぞれのラインセンスに従います．ThirdPartyLicenses.txt や COPYING などを確認してください．

