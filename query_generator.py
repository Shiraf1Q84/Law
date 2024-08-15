# query_generator.py
import openai

def generate_improved_query(original_query: str, api_key: str) -> tuple:
    openai.api_key = api_key
    prompt = f"""
    元の検索クエリ：{original_query}

    上記の検索クエリの意図をより深く理解し、法律用語や関連概念を含むより適切な検索クエリに改善してください。
    また、検索クエリの改善プロセスについて簡単に説明してください。

    改善された検索クエリ：
    改善プロセスの説明：
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは法律の専門家で、ユーザーの検索意図を深く理解し、適切な検索クエリを生成する能力があります。"},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        improved_query, explanation = content.split("改善プロセスの説明：")
        improved_query = improved_query.replace("改善された検索クエリ：", "").strip()
        explanation = explanation.strip()

        return improved_query, explanation
    except Exception as e:
        return str(e), "エラーが発生しました。APIキーが正しいことを確認してください。"