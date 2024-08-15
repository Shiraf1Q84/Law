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
        keywords = query.lower().split()
        results = []
        for doc in self.db.documents:
            score = sum(1 for keyword in keywords if keyword in doc['text'].lower())
            if score > 0:
                results.append((doc, score))
        return sorted(results, key=lambda x: x[1], reverse=True)

    def _merge_and_rank(self, keyword_results, vector_results):
        merged = {}
        for doc, score in keyword_results:
            merged[doc['text']] = {'document': doc, 'keyword_score': score, 'vector_score': 0}
        for doc, score in vector_results:
            if doc['text'] in merged:
                merged[doc['text']]['vector_score'] = score
            else:
                merged[doc['text']] = {'document': doc, 'keyword_score': 0, 'vector_score': score}
        
        results = list(merged.values())
        max_keyword = max((r['keyword_score'] for r in results), default=1)
        max_vector = max((r['vector_score'] for r in results), default=1)
        
        for r in results:
            keyword_score = r['keyword_score'] / max_keyword if max_keyword != 0 else 0
            vector_score = r['vector_score'] / max_vector if max_vector != 0 else 0
            r['score'] = (keyword_score + vector_score) / 2
        
        return sorted(results, key=lambda x: x['score'], reverse=True)
