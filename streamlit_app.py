import streamlit as st
from openai import OpenAI
import time

# Streamlit 설정
st.set_page_config(page_title="📖 Bible AI Chatbot", page_icon="🙏", layout="centered")

# ✅ Bible AI Chatbot 주요 특징 강조
st.title("📖 Bible AI Chatbot")
st.caption("✅ **간결한 챗봇 스타일** | ✅ **실시간 응답** | ✅ **개역성경 정확성 보장** | ✅ **한국어 지원**")

# OpenAI API 설정
openai_api_key = st.secrets["chatgpt"]
client = OpenAI(api_key=openai_api_key)

# ✅ 대화 이력 저장
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 성경 말씀을 찾아드리는 Bible AI Chatbot입니다. 무엇이든 물어보세요. 🙏"}]

# ✅ 채팅 UI 출력 (이전 대화 표시)
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ✅ 예상 질문 버튼 UI
st.subheader("📌 궁금한 내용을 선택하세요:")
question_options = {
    "인내에 대한 성경 말씀": "인내에 대한 성경 말씀은 무엇인가요?",
    "두려움을 극복하는 방법": "두려울 때 도움이 되는 성경 구절을 알려주세요.",
    "하나님의 사랑에 대한 구절": "하나님의 사랑을 느낄 수 있는 성경 구절이 있나요?",
}

# ✅ 버튼 클릭 시 해당 질문 자동 입력
selected_question = None
for key, value in question_options.items():
    if st.button(key, use_container_width=True):
        selected_question = value

# ✅ AI 응답 스트리밍 함수
def stream_bible_response():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "너는 기독교 AI 챗봇이며, 반드시 개역성경 번역본을 정확하게 인용해야 한다.\n"
                "1. 반드시 실제 존재하는 성경 구절의 **개역성경 번역본**만 제공하며, "
                "구글 검색 시 한 글자도 틀리지 않고 개역성경 내용이 검색 결과에 나와야 한다. "
                "반드시 (책 이름 장:절) 형식으로 출처를 정확히 표기하라.\n"
                "2. 구절이 길 경우, 일부만 제공하고 '...'을 사용하되 출처는 명확히 표기하라.\n"
                "3. 사용자에게 공감하는 어조를 유지하며, 짧은 위로 문장을 추가하라. "
                "(예: '힘드셨겠네요.', '주님께서 함께 하십니다.')\n"
                "4. 기독교적 존중을 담아 '성도님', '주님께서는...' 등의 표현을 활용하라.\n"
                "5. 출처가 명확하지 않을 경우, 대표적인 구절(예: '시편 23편')을 추천하라."
            )},
            *st.session_state.messages  # 기존 대화 내역 추가
        ],
        max_tokens=700,
        temperature=0.65,
        stream=True  # ✅ 스트리밍 응답 활성화
    )

    # ✅ `st.write_stream()`을 활용한 자연스러운 스트리밍
    for chunk in response:
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                yield delta.content  # 한 단어씩 반환하여 Streamlit에 표시
                time.sleep(0.02)  # 속도 조절

# ✅ 버튼 클릭 시 자동 입력 및 응답 시작
if selected_question:
    st.session_state.messages.append({"role": "user", "content": selected_question})
    st.chat_message("user").write(selected_question)

    # ✅ AI 응답 스트리밍 시작
    with st.chat_message("assistant"):
        st.write_stream(stream_bible_response())  # ✅ `st.write_stream()` 활용하여 자연스럽게 응답 표시
