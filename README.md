# nicovideo2discord
ニコニコ動画にある動画を閲覧したら、自動的にDiscord Rich Presenceで共有します。

## 使い方
### セットアップ
この拡張機能は３つのプログラムから形成されています。
1. コンテンツスクリプト (ブラウザ上で動作)
2. サーバー (Python3上で動作)
3. クライアント (Python3上で動作)

#### コンテンツスクリプト（ブラウザ拡張機能）のインストール
1. [拡張機能の管理画面](chrome://extensions/)に行きます。
2. 画面右上の「デベロッパーモード」をオンにします
3. 当レポジトリをcloneします
4. 好きなタグをチェックアウトします
5. 拡張機能の管理画面から、「パッケージ化されていない拡張機能をインストール」を押して、当レポジトリのbrowser-addonディレクトリを指定します

#### サーバーの準備
1. [このレポジトリ](https://github.com/okaits/nicovideo2discord)をcloneします
2. pipコマンドを利用可能な状態にして、次のコマンドを実行します
   ```bash
   python3 -m pip install -r ./requirements.txt
   ```

### 実行
#### コンテンツスクリプト
インストールした時点で既に自動的に動作するので、視聴前の準備は特に必要ありません。
下のサーバーとクライアントを起動すると、自動的にやってくれます。

#### サーバーとクライアントの実行
Discord Rich Presenceは変更にDiscordクライアントのRPCを使用するので、**Discordクライアント(アプリ)を起動してから**、start.pyを実行してください。

## Contributing

### License
[MIT License](LICENSE.md)
### Contributer
* [okaits#7534](https://info.okaits7534.mydns.jp)
