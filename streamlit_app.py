import streamlit as st
from openai import OpenAI
import time
import random
import json
import re 
import streamlit.components.v1 as components

from process.FUNCTION import format_bible_reference, get_bible_verse, replace_bible_references
from process.FUNCTION import module1, module2, stream_bible_response
from prompt.MANUAL_PROMPT import PROMPT_1, PROMPT_2
from data.QUESTION_POOL import question_pool
from data.BIBLE_BOOK_MAP import bible_book_map
from design.DESIGN_CODE import CSS_DESIGN

# ✅ Streamlit 설정
st.set_page_config(page_title="📖 Bible AI Chatbot", page_icon="🙏", layout="centered")

# ✅ 디자인
st.markdown(CSS_DESIGN, unsafe_allow_html=True)

# ✅ 타이틀 설정
st.title("📖 Bible AI Chatbot")
st.caption("✅ **간결한 챗봇 스타일** | ✅ **실시간 응답** | ✅ **개역성경 정확성 보장** | ✅ **한국어 지원**")

# ✅ OpenAI API 설정
openai_api_key = st.secrets["chatgpt"]
client = OpenAI(api_key=openai_api_key)


USER_NICKNAME = "성도님"
USER_AVATAR = "👤"  # 사용자 아이콘 (URL 가능)
AI_AVATAR = "📖"  # AI 아이콘 (URL 가능)

# 성경 JSON 데이터 로드
def load_bible_json():
    with open("data/bible.json", "r", encoding="utf-8") as f:
        return json.load(f)

bible_data = load_bible_json()


##### MAIN CHAT ENVIRONMENT ########

# ✅ 후속 질문 기능을 위한 상태 초기화
if "follow_up" not in st.session_state:
    st.session_state.follow_up = None

# ✅ 대화 이력 저장
if "messages" not in st.session_state:
    st.session_state.messages = []


# ✅ 현재 표시할 질문 리스트 (9개씩 랜덤 출력)
if "question_list" not in st.session_state or not st.session_state.question_list:
    st.session_state.question_list = random.sample(question_pool, 9)

st.subheader("📌 신앙과 삶의 고민이 있다면, 마음을 나누어 보세요.")

chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user", avatar=USER_AVATAR).write(f"**[{USER_NICKNAME}]** {msg['content']}")
        else:
            st.chat_message("assistant", avatar=AI_AVATAR).write(f"**[한줄성경]** {msg['content']}")

# ✅ 자연어 입력 필드 (항상 아래 유지)
user_input = st.text_input("질문을 입력하세요:", placeholder="예: 하나님을 신뢰하는 법을 알고 싶어요.")

# ✅ 3열 배치 (총 9개 질문 버튼) - 입력 필드 아래에 배치
selected_question = None
question_container = st.container()

with question_container:
    cols = st.columns(3)  
    for i, q in enumerate(st.session_state.question_list):
        with cols[i % 3]:  
            if st.button(q, use_container_width=True):
                selected_question = q

# ✅ 질문 선택 또는 자연어 입력 시 응답 시작
if selected_question or user_input:
    user_query = selected_question if selected_question else user_input
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with chat_container:
        st.chat_message("user", avatar=USER_AVATAR).write(f"**[{USER_NICKNAME}]** {user_query}")

    # ✅ AI 응답 스트리밍 시작 (이전 대화 삭제 없이 유지)
    with chat_container:
        st.chat_message("assistant", avatar=AI_AVATAR).write_stream(stream_bible_response(user_query))

    # ✅ 새로운 질문 리스트를 갱신하지 않음 (기존 질문 유지)

# ✅ 새로운 질문 리스트 갱신 버튼 (사용자가 원할 때만 변경)
if st.button("🔄 새로운 질문 리스트 보기", use_container_width=True):
    st.session_state.question_list = random.sample(question_pool, 9)
