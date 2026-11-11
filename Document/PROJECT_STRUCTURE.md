# MTG Card Viewer - Project Structure

```text
CardViewer/
├── Src/
│   ├── mtg/
│   │   ├── __init__.py
│   │   ├── mtg_card_search.py
│   │   ├── mtg_card_viewer_server.py
│   │   └── mtg_card_viewer_window.py
│   ├── tests/
│   │   └── test_japanese_search.py
│   ├── mtg_card_viewer.py
│   ├── start_card_viewer.bat
│   ├── build_card_viewer.bat
│   └── build_card_viewer_simple.bat
├── Document/
│   ├── BUILD_SUMMARY.txt
│   ├── JAPANESE_SEARCH.md
│   ├── PROJECT_STRUCTURE.md
│   ├── QUICKSTART.txt
│   ├── SUMMARY.txt
│   └── UI_OPTIMIZATION.md
├── build/
│   └── MTGCardViewerApp.spec
├── release/
│   ├── MTGCardViewerApp.exe
│   └── README.txt
├── mtg_card_viewer.html
├── requirements.txt
├── requirements-build.txt
└── README.md
```

## ディレクトリとファイル

- `Src/mtg/` は Scryfall 検索、HTTP サーバー、Windows ウィンドウの実装です。
- `Src/mtg_card_viewer.py` はアプリケーションのエントリーポイントです。
- `Src/tests/` はテスト用ファイルの配置先です。
- `Document/` はユーザー向けおよび開発者向けドキュメントです。
- `build/` は PyInstaller の設定と中間生成物を格納します。
- `release/` は配布用の実行ファイルを格納します。
- `mtg_card_viewer.html` はアプリが表示する UI です。
- `requirements.txt` と `requirements-build.txt` はルートからインストールします。

## 起動とビルド

ソースから起動するには、ルートで依存パッケージをインストールしてから `Src/start_card_viewer.bat` を実行します。

```powershell
python -m pip install -r requirements.txt
.\Src\start_card_viewer.bat
```

実行ファイルを再ビルドするには、ビルド用依存パッケージをインストールして `Src/build_card_viewer.bat` を実行します。

```powershell
python -m pip install -r requirements-build.txt
.\Src\build_card_viewer.bat
```

テストは次のコマンドで実行できます。

```powershell
python -m unittest discover -s Src/tests -v
```
