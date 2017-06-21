# s2speech (scratchで音声合成)

## インストール

1. s2aspeech のインストール
    1. https://github.com/memakura/s2speech/dist/s2speech-0.1-amd64.msi にて [Download] を選ぶ
    1. ダウンロードされた s2speech-0.1-amd64.msi を実行
        1. Windows8以上では「WindowsによってPCが保護されました」と出る場合があるので，[詳細情報] をクリックして [実行]
        1. Windows7では「発行元が不明」と出るが[実行]
        1. （このほかウイルスチェックソフトでも発行元が不明に関して何かしら警告が出る可能性あり）
    1. インストール先の例: "C:\Program Files\s2speech" (以下ではここにインストールしたことを仮定)

## 使用方法

1. デモ : "C:\Program Files\s2speech\scratch/project.sb2"
1. 使い方
    1. Scratch2 offline editor を立ち上げる
    1. シフトキーを押しながら「ファイル」を押し「実験的なHTTP拡張を読み込み」を選ぶ
    1. "C:\Program Files\s2speech\scratch\s2speech_JP.s2e" を選択（このファイルは別の分かりやすい場所にコピーしておいてもよい)
1. デスクトップ上の s2speech を立ち上げて，最後に「Running on http://127.0.0.1:50210」が表示されれば起動完了

## htsvoices の追加

README.md 参照のこと
