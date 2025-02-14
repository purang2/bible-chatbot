from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os


from retrieval import replace_bible_references, extract_bible_references, get_verse_context  # 후처리 모듈 임포트
from prompt import SYSTEM_PROMPT  # 프롬프트 불러오기


# ✅ .env 파일 로드
load_dotenv(override=True)


app = Flask(__name__)
CORS(app, resources={
    r"/chat": {
        "origins": ["http://localhost:3000"],  # React 개발 서버 주소
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"message": "질문을 입력해 주세요."}), 400

        user_input = data['message'].strip()
        if not user_input:
            return jsonify({"message": "질문을 입력해 주세요."}), 400

        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=550
        )
        
        parsed_response = extract_bible_references(replace_bible_references(completion.choices[0].message.content))

        return jsonify({
            "main_message": parsed_response["main_message"],
            "verses": parsed_response["verses"]
        }), 200

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "message": "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
        }), 500


@app.route("/verse-context/<book>/<chapter>/<verse>", methods=["GET"])
def verse_context_endpoint(book, chapter, verse):
    result, status_code = get_verse_context(book, chapter, verse)
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True, port=5000)