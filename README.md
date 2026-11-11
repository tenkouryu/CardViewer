# MTG Card Viewer

Magic: The Gathering のカードを検索し、画像やカード情報を表示する Windows 向けビューアーです。カード名（英語・日本語）またはセットコードとコレクター番号で検索できます。カード情報と画像の取得には Scryfall API を使用するため、インターネット接続が必要です。

## 主な機能

- カード名で検索（英語・日本語）
- セットコードとコレクター番号で検索
- 入力中のカード名候補表示
- カード画像、タイプ、マナコスト、ルールテキストなどの表示
- ダークモードとレスポンシブレイアウト
- Scryfall のカード詳細ページへのリンク

## 起動方法

### Windows アプリ版

1. [`release/MTGCardViewerApp.exe`](release/MTGCardViewerApp.exe) を起動します。
2. 検索画面が表示されたら、カード名またはセット情報を入力します。

Python のインストールは不要です。Microsoft Edge WebView2 Runtime とインターネット接続が必要です。

### ソースコードから起動

Windows で Python 3.9 以降を用意し、リポジトリのルートで依存パッケージをインストールします。

```powershell
python -m pip install -r requirements.txt
```

次に、起動用バッチファイルを実行します。

```powershell
.\Src\start_card_viewer.bat
```

または、次のように Python から直接起動できます。

```powershell
Set-Location Src
python mtg_card_viewer.py
```

ソースコードから起動する場合も WebView2 Runtime とインターネット接続が必要です。

## 使い方

### カード名で検索

カード名を入力して候補を選ぶか、検索を実行します。英語名（例: `Lightning Bolt`）と日本語名（例: `稲妻`）を入力できます。

### セットコードとコレクター番号で検索

セットコード（例: `neo`）とコレクター番号（例: `129`）を入力して検索します。

## 開発

主なファイルは次のとおりです。

```text
.
├── mtg_card_viewer.html       # UI
├── Src/
│   ├── mtg_card_viewer.py     # 起動エントリーポイント
│   ├── start_card_viewer.bat  # Windows 用起動スクリプト
│   └── mtg/                   # 検索処理、HTTP サーバー、ウィンドウ
├── requirements.txt           # 実行時依存パッケージ
├── requirements-build.txt     # ビルド用依存パッケージ
├── Document/                  # 追加ドキュメント
├── build/                     # PyInstaller の中間ファイル
├── release/
│   └── MTGCardViewerApp.exe   # 配布用アプリ
```

PyInstaller で実行ファイルをビルドする場合は、ビルド用依存パッケージをインストールしてからビルドスクリプトを実行します。

```powershell
python -m pip install -r requirements-build.txt
.\Src\build_card_viewer.bat
```

詳しい構成や検索仕様については、[`Document/PROJECT_STRUCTURE.md`](Document/PROJECT_STRUCTURE.md) と [`Document/JAPANESE_SEARCH.md`](Document/JAPANESE_SEARCH.md) を参照してください。

## 外部サービスと商標

- カードデータおよび画像は [Scryfall API](https://scryfall.com/docs/api) から取得します。利用時は [Scryfall の API 利用規約](https://scryfall.com/docs/api) に従ってください。
- Magic: The Gathering は Wizards of the Coast の商標です。
