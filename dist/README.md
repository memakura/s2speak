# s2speech インストーラ
scratchで音声合成 (OpenJTalk を scratch 2 オフラインエディタから呼ぶ)

![s2speech](https://github.com/memakura/s2speech/blob/master/images/ScratchSpeechSynth.png)
![block_and_sample](https://github.com/memakura/s2speech/blob/master/images/block_and_sample_JP.png)


## インストール
1. https://github.com/memakura/s2speech/blob/master/dist/s2speech-0.2-amd64.msi にて [Download] を選ぶ
    - msiファイルおよびインストールされるファイル一式はいずれもサイズが大きい（100MB以上は必要）
1. ダウンロードされた msi ファイルを実行
    1. Windows8以上では「WindowsによってPCが保護されました」と出る場合があるので，[詳細情報] をクリックして [実行]
    1. Windows7では「発行元が不明」と出るが[実行]
    1. （このほかウイルスチェックソフトでも発行元が不明に関して何かしら警告が出る可能性あり）
1. インストール先の例: "C:\Program Files\s2speech" (以下ではここにインストールしたことを仮定)

## s2speechの起動方法
- デスクトップ上の s2speech を立ち上げて「==== Running on http://127.0.0.1:50210 ====」が表示されれば起動完了
    1. voices.cfg で登録されている「声の番号 : 声の名前」のリストが起動時に表示される
    1. 正しく起動されていれば，Scratch の「その他」ブロックの s2speechにて赤丸から緑丸になる

## Scratchでの書き方
- 以下のデモが参考になる
    - "C:\Program Files\s2speech\00scratch/project.sb2"
- 新たに作成するとき
    1. Scratch2 offline editor でシフトキーを押しながら「ファイル」->「実験的なHTTP拡張を読み込み」を選ぶ
    1. "C:\Program Files\s2speech\00scratch\s2speech_JP.s2e" を選択して開く（このファイルは別の分かりやすい場所にコピーしておいてもよい)

## 声の追加や変更 (htsvoices)
1. 追加の .hts ファイルもしくはフォルダを "C:\Users\(ユーザ名)\AppData\Local\s2speech\htsvoices" に置き，同フォルダに voices.cfg を作成する
    - 初めて実行したときに htsvoicesフォルダは自動作成される
    - htsファイルの置き方や voices.cfg の作成は "C:\Program Files\s2speech\htsvoices" を参考にする
    - "C:\Program Files\s2speech\htsvoices" に追加する形で読まれる (voice_id の番号も追加されて順にふられる)
1. 必要に応じて 00scratch\s2speech_JP.s2e をコピー・編集して読み込んでおく (voice_id の番号追加など)
1. s2speech.py を実行する

## Notes
- Original python-jtalk scripts are from https://github.com/nvdajp/python-jtalk/
- jtalk directory is from nvdajp
- Mecab and OpenJTalk DLLs were compiled with 64bit
