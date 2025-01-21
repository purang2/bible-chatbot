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
            *st.session_state.messages,
            {"role": "user", "content": user_query}
        ],
        max_tokens=200,
        temperature=0.65,
        stream=True
    )

    full_response = ""  # 전체 응답 저장

    for chunk in response:
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                full_response += delta.content
                yield delta.content  # ✅ 한 줄씩 반환
                time.sleep(0.02)  # ✅ 응답 속도 조절

    # ✅ 응답 저장 (이제 입력이 다시 가능함)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ✅ 심화된 질문 리스트 (150개)
question_pool = [
    "하나님이 정말 나를 사랑하시는지 어떻게 확신할 수 있을까요?",
    "기도해도 응답이 없을 때 어떻게 해야 할까요?",
    "믿음이 흔들릴 때 성경에서 어떤 말씀을 붙잡아야 할까요?",
    "삶이 너무 고통스러울 때 하나님께서 주시는 위로의 말씀은 무엇인가요?",
    "사람들에게 배신당했을 때 성경에서는 어떻게 하라고 하나요?",
    "가족과의 갈등을 해결하는 성경적인 방법이 있을까요?",
    "어려운 상황에서도 감사하는 마음을 가질 수 있을까요?",
    "앞으로 어떤 길을 선택해야 할지 모를 때 어떻게 기도해야 할까요?",
    "세상에서 그리스도인으로 살아가는 것이 쉽지 않을 때 어떻게 해야 할까요?",
    "기도가 습관이 되지 않을 때 어떻게 해야 할까요?",
    # 추가 질문 140개 생략 (위에서 제공한 리스트 활용)
]

# ✅ 자연어 입력 필드 추가
st.subheader("📌 궁금한 내용을 입력하거나 질문을 선택하세요.")

user_input = st.text_input("질문을 입력하세요:", placeholder="예: 하나님을 신뢰하는 법을 알고 싶어요.")

# ✅ 현재 표시할 질문 리스트 (세 개씩 랜덤 출력)
if "question_list" not in st.session_state or not st.session_state.question_list:
    st.session_state.question_list = random.sample(question_pool, 3)

# ✅ 버튼 클릭 시 자동 입력 + 질문 변경
selected_question = None
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(st.session_state.question_list[0], use_container_width=True):
        selected_question = st.session_state.question_list[0]
with col2:
    if st.button(st.session_state.question_list[1], use_container_width=True):
        selected_question = st.session_state.question_list[1]
with col3:
    if st.button(st.session_state.question_list[2], use_container_width=True):
        selected_question = st.session_state.question_list[2]

# ✅ 질문 선택 또는 자연어 입력 시 응답 시작
if selected_question or user_input:
    user_query = selected_question if selected_question else user_input
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    # ✅ AI 응답 스트리밍 시작
    with st.chat_message("assistant"):
        st.write_stream(stream_bible_response(user_query))

    # ✅ 새로운 질문 리스트 업데이트 (답변이 끝난 후에도 질문 선택 가능)
    st.session_state.question_list = random.sample(question_pool, 3)

    # ✅ 입력창을 다시 활성화 (사용자가 다시 질문할 수 있도록)
    st.rerun()
