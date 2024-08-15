# 著作権法検索アプリケーション

このアプリケーションは、自然言語処理を使用して著作権法に関連する法文を検索するためのツールです。Streamlitを使用したユーザーインターフェースと、Pineconeベクトルデータベースを利用した高速な検索機能を提供します。

## 機能

- 自然言語による法文検索
- インタラクティブなWebインターフェース
- 高速なベクトル類似度検索

## セットアップ

1. リポジトリをクローンします：
   ```
   git clone https://github.com/yourusername/copyright-law-search-app.git
   cd copyright-law-search-app
   ```

2. 仮想環境を作成し、アクティベートします：
   ```
   python -m venv venv
   source venv/bin/activate  # Linuxまたは macOS
   # または
   venv\Scripts\activate  # Windows
   ```

3. 必要なパッケージをインストールします：
   ```
   pip install -r requirements.txt
   ```

4. Pineconeアカウントを作成し、API keyを取得します。

5. `app.py`ファイル内の`YOUR_API_KEY`と`YOUR_ENVIRONMENT`をPineconeの設定に合わせて更新します。

## 使用方法

1. アプリケーションを起動します：
   ```
   streamlit run app.py
   ```

2. ブラウザで表示されるURLにアクセスします（通常は http://localhost:8501 ）。

3. サイドバーの「データベースの初期化」ボタンをクリックして、Pineconeデータベースを設定します。

4. 検索フィールドにキーワードや文章を入力し、「検索」ボタンをクリックします。

5. 関連する法文が表示されます。

## 注意事項

- このアプリケーションは、デモンストレーション目的で作成されています。実際の法的アドバイスには使用しないでください。
- 現在のバージョンでは、限られた数の法文のみが含まれています。実際の使用では、より包括的なデータベースを使用することをお勧めします。

## ライセンス

このプロジェクトは [MITライセンス](https://opensource.org/licenses/MIT) の下で公開されています。

## 貢献

プルリクエストは歓迎します。大きな変更を加える場合は、まずissueを開いて議論してください。

## 連絡先

質問や提案がある場合は、[issues](https://github.com/yourusername/copyright-law-search-app/issues)を開いてください。
