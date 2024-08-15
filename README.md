# 法文横断検索システム

このプロジェクトは、法文の横断検索を行うためのテスト環境を提供します。PDFファイルから法文を抽出し、ベクトル化して検索可能にします。

## 機能

- PDFファイルからのテキスト抽出
- テキストのチャンク分割とベクトル化
- キーワード検索とベクトル検索の組み合わせ
- 検索結果のランキング付けと表示
- シンプルなWeb UIによる検索インターフェース

## セットアップ

1. リポジトリをクローンします：

   ```
   git clone https://github.com/yourusername/law-search-system.git
   cd law-search-system
   ```

2. 仮想環境を作成し、アクティベートします：

   ```
   python -m venv venv
   source venv/bin/activate  # Linuxの場合
   venv\Scripts\activate  # Windowsの場合
   ```

3. 必要な依存関係をインストールします：

   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. サンプルのPDFファイル（`sample_law.pdf`）をプロジェクトのルートディレクトリに配置します。

2. アプリケーションを実行します：

   ```
   streamlit run main.py
   ```

3. ブラウザで表示されるURLにアクセスし、検索インターフェースを使用します。

## プロジェクト構造

- `main.py`: メインスクリプト
- `pdf_processor.py`: PDFファイル処理モジュール
- `vector_database.py`: ベクトルデータベース実装
- `search_engine.py`: 検索エンジン実装
- `ui.py`: Streamlitを使用したUI実装

## 今後の展開

- 検索精度の向上
- Pineconeとの連携
- より高度なUIの実装

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は`LICENSE`ファイルを参照してください。

---

# requirements.txt

pymupdf==1.19.0
scikit-learn==0.24.2
streamlit==0.89.0
numpy==1.21.2
