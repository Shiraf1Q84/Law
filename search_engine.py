# search_engine.py
from typing import List
import re

class SearchEngine:
    def __init__(self, db: VectorDatabase):
        self.db = db

    def search(self, query: str) -> List[dict]:
        # キーワード検索とベクトル検索を実行
        keyword_results = self._keyword_search(query)
        vector_results = self.db.search(query)
        
        # 結果をマージしてランキング
        merged_results = self._merge_and_rank(keyword_results, vector_results)
        
        # 上位10件を返す
        return merged_results[:10]

    def _keyword_search(self, query: str) -> List[dict]:
        # 簡易的なキーワード検索の実装
        keywords = query.lower().split()
        results = []
        for doc in self.db.documents:
            score = sum(1 for keyword in keywords if keyword in doc['text'].lower())
            if score > 0:
                results.append((doc, score))
        return sorted(results, key=lambda x: x[1], reverse=True)

    def _merge_and_rank(self, keyword_results, vector_results):
        # キーワード検索結果とベクトル検索結果をマージしてランキング
        pass