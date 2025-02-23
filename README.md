# nicovideo2discord
ニコニコ動画を視聴する際に、自動的にDiscord Rich Presenceで共有する拡張機能です。 
Ubuntu 24.04のChromiumで動作確認をしています。
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

## 使い方
ブラウザから直接Discordにいろいろするのは難しいので、Python3でHTTPサーバーを建ててそこらへんを代わりにいろいろしてもらう、という構造になっています。

### Requirements
* PC
* ブラウザ
* Discord（Web版不可）

### 初期設定
1. ソースコードをダウンロード  
   [最新リリース](https://github.com/okaits/nicovideo2discord/releases/latest)から、`Source code (zip)`をダウンロードし、展開する。
2. ブラウザに拡張機能をインストール  
    （Chromium系の場合）`chrome://extensions`を開き、右上の「デベロッパー モード」をONにし、左上の「パッケージ化されていない拡張機能を読み込む」を押し、先ほどダウンロードしたソースコードの`browser_addon`フォルダーを選択する。
3. サーバーのダウンロード
   [最新リリース](https://github.com/okaits/nicovideo2discord/releases/latest)から、Windowsなら`windows_amd64_executable_server.exe`を、Linuxなら`linux_amd64_executable_server.elf`をダウンロードする。

### 使用
#### Windows
1. Discordを開く
2. 初期設定時にダウンロードした`windows_amd64_executable_server.exe`をダブルクリック（実行）する。
3. 初回のみ「WindowsによってPCが保護されました」というダイアログが表示されることがあるので、「詳細情報」をクリックすることで右下に現れる実行ボタンを押して実行する。
4. 動画を観る
#### Linux
1. Discordを開く
2. 初期設定時にダウンロードした`linux_amd64_executable_server.elf`に、付与されていない場合は実行権限を付与し、実行する。
3. 動画を観る
#### 開発者向け
1. Discordを開く
2. `python3 -m poetry run python3 server.py`  
    リポジトリにcdしてから、サーバーを起動する。
3. 動画を観る

### License
[MIT License](LICENSE.md)
### Contributer
* [okaits#7534](https://www.okaits7534.net/)
