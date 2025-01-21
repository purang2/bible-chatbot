import streamlit as st
from openai import OpenAI
import time
import random

# Streamlit 설정
st.set_page_config(page_title="📖 Bible AI Chatbot", page_icon="🙏", layout="centered")

# ✅ Bible AI Chatbot 주요 특징 강조
st.title("📖 Bible AI Chatbot")
st.caption("✅ **간결한 챗봇 스타일** | ✅ **실시간 응답** | ✅ **개역성경 정확성 보장** | ✅ **한국어 지원**")

# OpenAI API 설정
openai_api_key = st.secrets["chatgpt"]
client = OpenAI(api_key=openai_api_key)

# ✅ 대화 이력 저장 (시스템 메시지 제거)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ 채팅 UI 출력 (이전 대화 표시)
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ✅ AI 응답 스트리밍 함수
def stream_bible_response(user_query):
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
            *st.session_state.messages,  # 기존 대화 내역 추가
            {"role": "user", "content": user_query}
        ],
        max_tokens=700,
        temperature=0.65,
        stream=True  # ✅ 스트리밍 응답 활성화
    )

    # ✅ `st.write_stream()`을 활용한 자연스러운 스트리밍
    streamed_text = ""
    for chunk in response:
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                streamed_text += delta.content
                yield streamed_text  # 한 단어씩 반환하여 Streamlit에 표시
                time.sleep(0.02)  # 속도 조절

    # ✅ 응답 저장 (채팅 내역 유지)
    st.session_state.messages.append({"role": "assistant", "content": streamed_text})

# ✅ 예상 질문 (계속 바뀌도록 랜덤 리스트 적용)
question_pool = [
    "인내에 대한 성경 말씀은 무엇인가요?",
    "두려움을 극복하는 방법은?",
    "하나님의 사랑을 느낄 수 있는 성경 구절이 있나요?",
    "슬플 때 위로가 되는 성경 말씀을 알려주세요.",
    "하나님을 신뢰하는 법에 대해 알려주세요.",
    "어려운 시기를 겪을 때 읽으면 좋은 성경 구절이 있나요?",
    "평안함을 얻기 위한 성경 말씀은 무엇인가요?",
]

# ✅ 현재 표시할 질문 리스트 (세 개씩 보여주기)
if "question_list" not in st.session_state or not st.session_state.question_list:
    st.session_state.question_list = random.sample(question_pool, 3)

# ✅ 버튼 클릭 시 자동 입력 + 질문 변경
st.subheader("📌 궁금한 내용을 선택하세요:")
selected_question = None
for q in st.session_state.question_list:
    if st.button(q, use_container_width=True):
        selected_question = q

# ✅ 질문 선택 시 응답 시작 + 질문 리스트 업데이트
if selected_question:
    st.session_state.messages.append({"role": "user", "content": selected_question})
    st.chat_message("user").write(selected_question)

    # ✅ AI 응답 스트리밍 시작
    with st.chat_message("assistant"):
        st.write_stream(stream_bible_response(selected_question))

    # ✅ 새로운 질문 리스트 업데이트 (사용자가 볼 때 질문이 계속 바뀜)
    st.session_state.question_list = random.sample(question_pool, 3)
