# 日本語検索対応について

## 検索方法（推奨順）

### 1️⃣ セット + コレクター番号（最推奨 ✓✓✓）
```
セットコード: neo
番号: 129
```
**最も確実で高速です。日本語/英語関係なく動作します。**

### 2️⃣ 英語カード名で検索 ✓
```
例: Lightning Bolt
   Island
```
**Scryfallデータベースは英語が基本。最も安定。**

### 3️⃣ 日本語カード名での検索 ✓

日本語カード名での検索にも対応しています。

```
例: 稲妻
   島
```

**動作方法：**
- 日本語カード名を直接入力
- Scryfallのfuzzyマッチングで検索
- 日本語版カード情報を表示

## 実装例

### 日本語カード名を英語に確認する方法

1. **Scryfallサイトで検索**
   ```
   https://scryfall.com/
   ```

2. **日本語版を探す**
   - 検索結果からセット+番号を確認
   - MTG Card Viewerで入力

### セットコード一覧

```
neo  = Kamigawa: Neon Dynasty
ltr  = The Lord of the Rings
m21  = Core Set 2021
```

Scryfallのセットリスト：https://scryfall.com/sets

## トラブルシューティング

### 「見つかりません」エラー

**原因：**
- Scryfallに登録されていない
- セットコード/番号が間違っている

**解決策：**
1. Scryfallサイトで確認
2. セット+番号で検索
3. 公式カードリストを参照

## 関連リンク

- **Scryfall**: https://scryfall.com
- **MTGデータベース**: https://mtg.fandom.com/


