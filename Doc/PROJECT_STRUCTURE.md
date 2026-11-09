# MTG Card Viewer - Project Structure

```
MTGCardViewer/
├── src/
│   ├── mtg/
│   │   ├── __init__.py                    # パッケージ初期化
│   │   ├── mtg_card_search.py             # Scryfall API処理
│   │   ├── mtg_card_viewer_server.py      # HTTPサーバー実装
│   │   └── mtg_card_viewer_window.py      # Windowsアプリ用ラッパー
│   ├── tests/
│   │   └── (テストファイル用フォルダ)
│   ├── mtg_card_viewer.py                 # メインエントリポイント
│   └── start_card_viewer.bat              # 起動用バッチファイル
│
├── mtg_card_viewer.html                   # UIファイル（ルート）
├── requirements.txt                       # Python依存パッケージ
├── README.md                              # 詳細ドキュメント
├── SUMMARY.txt                            # プロジェクト概要
└── PROJECT_STRUCTURE.md                   # このファイル
```

## ディレクトリ説明

### `/src` - ソースコードフォルダ
アプリケーションのメインコードが格納されています。

### `/src/mtg/` - メインパッケージ
MTG Card Viewerのコア機能を実装したPythonパッケージです。

- **`__init__.py`** - パッケージ初期化ファイル。公開APIを定義します。
- **`mtg_card_search.py`** - Scryfall APIとの通信を管理します。
  - `fetch_card_by_name()` - カード名での検索
  - `fetch_card_by_set_number()` - セット+番号での検索
  - `search_cards_by_name()` - パターンマッチング検索
  
- **`mtg_card_viewer_server.py`** - HTTPサーバー実装
  - `CardViewerHandler` - リクエスト処理
  - `/api/card/search` - カード検索エンドポイント
  - `/api/card/set` - セット検索エンドポイント
  - `/api/search` - 補完検索エンドポイント
  
- **`mtg_card_viewer_window.py`** - Windows用ウィンドウラッパー
  - `EmbeddedCardViewerHandler` - pywebview用ハンドラ
  - `main()` - アプリケーション起動関数

### `/src/tests/` - テストフォルダ
自動テストを配置するためのフォルダです（現在は空）。

### `/src` - ルートスクリプト
- **`mtg_card_viewer.py`** - メインエントリポイント
  - `from mtg.mtg_card_viewer_window import main` でアプリを起動
  
- **`start_card_viewer.bat`** - Windows用起動スクリプト
  - チャーセット設定（UTF-8）
  - Python実行
  - 終了時にポーズ

### `mtg_card_viewer.html` - UIファイル（ルート）
フロントエンドのHTML/CSS/JavaScriptコード。
HTTPサーバーから提供されます。

## インポート構造

```
mtg_card_viewer.py
  └── mtg.mtg_card_viewer_window.main()
      └── mtg.mtg_card_viewer_server.CardViewerHandler
          └── mtg.mtg_card_search (fetch_card_by_name など)
```

## 実行フロー

```
1. start_card_viewer.bat
   ↓
2. python mtg_card_viewer.py
   ↓
3. mtg.mtg_card_viewer_window.main()
   ↓
4. ThreadingHTTPServer起動 + pywebview ウィンドウ作成
   ↓
5. ユーザーがブラウザで検索
   ↓
6. /api/card/search → mtg_card_viewer_server.py
   ↓
7. mtg_card_search.py で Scryfall API呼び出し
   ↓
8. JSON結果をフロントエンドに返す
   ↓
9. mtg_card_viewer.html で画面に表示
```

## モジュール間依存関係

```
mtg_card_viewer.py (エントリポイント)
    ↓
mtg_card_viewer_window.py (Windowsアプリ化)
    ↓
mtg_card_viewer_server.py (HTTPハンドラ)
    ↓
mtg_card_search.py (API処理)
    ↓
Scryfall API (外部)
```

## 起動方法

### Windows版（バッチファイル）
```bash
cd src
start_card_viewer.bat
```

### Pythonコマンドラインから
```bash
cd src
python mtg_card_viewer.py
```

### モジュールとしてインポート
```python
from mtg.mtg_card_search import fetch_card_by_name
card = fetch_card_by_name("Lightning Bolt")
```

## 今後の拡張

テストを追加する場合は `src/tests/` に配置してください：
```
src/tests/
├── __init__.py
├── test_mtg_card_search.py
├── test_mtg_card_viewer_server.py
└── ...
```

テスト実行:
```bash
python -m unittest discover -s src/tests -v
```
