import openai
from openai import OpenAIError

def generate_improved_query(original_query: str, api_key: str) -> tuple:
    client = openai.OpenAI(api_key=api_key)
    prompt = f"""
    元の検索クエリ：{original_query}

    上記の検索クエリの意図をより深く理解し、法律用語や関連概念を含むより適切な検索クエリに改善してください。
    また、検索クエリの改善プロセスについて簡単に説明してください。

    改善された検索クエリ：
    改善プロセスの説明：
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "あなたは法律の専門家で、ユーザーの検索意図を深く理解し、適切な検索クエリを生成する能力があります。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300,
            response_format={"type": "text"}
        )

        content = response.choices[0].message.content
        improved_query, explanation = content.split("改善プロセスの説明：")
        improved_query = improved_query.replace("改善された検索クエリ：", "").strip()
        explanation = explanation.strip()

        return improved_query, explanation
    except OpenAIError as e:
        error_message = f"OpenAI APIエラー: {str(e)}"
        if "invalid_api_key" in str(e):
            error_message += "\nAPIキーが正しくありません。正しいAPIキーを入力してください。"
        elif "insufficient_quota" in str(e):
            error_message += "\nAPIの使用量制限に達しました。請求情報を確認するか、制限をアップグレードしてください。"
        return None, error_message
    except Exception as e:
        return None, f"予期せぬエラーが発生しました: {str(e)}"
