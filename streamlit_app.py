import streamlit as st
from openai import OpenAI
import time
import random


# ✅ Streamlit 설정
st.set_page_config(page_title="📖 Bible AI Chatbot", page_icon="🙏", layout="centered")

# ✅ Pretendard 폰트 적용 (CSS 삽입)
st.markdown("""
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/Pretendard/dist/web/static/pretendard.css');

        * {
            font-family: 'Pretendard', sans-serif;
        }

        /* 채팅 메시지 스타일 */
        .stChatMessage {
            font-family: 'Pretendard', sans-serif !important;
            font-size: 16px;
            line-height: 1.6;
        }

        /* 입력창 스타일 */
        .stTextInput input {
            font-family: 'Pretendard', sans-serif !important;
            font-size: 14px;
        }

        /* 버튼 스타일 */
        .stButton > button {
            font-family: 'Pretendard', sans-serif !important;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)


# ✅ Bible AI Chatbot 주요 특징 강조
st.title("📖 Bible AI Chatbot")
st.caption("✅ **간결한 챗봇 스타일** | ✅ **실시간 응답** | ✅ **개역성경 정확성 보장** | ✅ **한국어 지원**")

# ✅ OpenAI API 설정
openai_api_key = st.secrets["chatgpt"]
client = OpenAI(api_key=openai_api_key)

# ✅ 닉네임 설정 (최초 실행 시 입력 가능)
if "nickname" not in st.session_state:
    st.session_state.nickname = st.text_input("닉네임을 입력하세요:", value="성도님")

USER_NICKNAME = st.session_state.nickname  # 사용자 닉네임 저장
USER_AVATAR = "👤"  # 사용자 아이콘 (URL 가능)
AI_AVATAR = "📖"  # AI 아이콘 (URL 가능)

# ✅ 후속 질문 기능을 위한 상태 초기화
if "follow_up" not in st.session_state:
    st.session_state.follow_up = None

# ✅ 대화 이력 저장
if "messages" not in st.session_state:
    st.session_state.messages = []


# ✅ AI 응답 스트리밍 함수
def stream_bible_response(user_query):
    prefixed_query = (
        "[개역성경 번역본]에서 정확한 인용과 출처(책 이름 장:절)를 명확히 표기하며, "
        "공감하는 어조와 기독교적 존중을 담아 답변해 주세요.\n\n" + user_query
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            *st.session_state.messages,
            {"role": "user", "content": prefixed_query}
        ],
        max_tokens=500,
        temperature=1.25,
        stream=True  # ✅ 스트리밍 활성화
    )

    full_response = ""  # 전체 응답 저장

    for chunk in response:
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                full_response += delta.content
                yield delta.content  # ✅ 한 줄씩 반환
                time.sleep(0.028)  # ✅ 응답 속도 조절

    # ✅ 응답 저장 (대화 내역 유지)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ✅ 질문 리스트 (50개)
question_pool = [
    # 🔹 인간관계 고민
    "가족과의 갈등을 어떻게 풀어야 할까요?",
    "친구에게 상처를 받았을 때 어떻게 하면 좋을까요?",
    "배신당한 기분에서 벗어나려면 어떻게 해야 할까요?",
    "사람들에게 쉽게 마음을 열지 못하는데, 어떻게 하면 좋을까요?",
    "연인과의 관계에서 신뢰가 깨졌을 때 어떻게 해야 할까요?",
    "누군가를 용서하는 게 너무 어려운데, 방법이 있을까요?",
    "내가 너무 의존적인 관계를 맺고 있는 건 아닐까요?",
    "진정한 친구를 찾는 게 너무 어려워요.",
    "부모님과의 가치관 차이로 힘들 때 어떻게 해야 할까요?",
    "혼자가 편한데, 그래도 사람을 만나야 할까요?",

    # 🔹 삶의 방향 & 미래 고민
    "내가 지금 가고 있는 길이 맞는 걸까요?",
    "하고 싶은 일이 없는데, 어떻게 살아가야 할까요?",
    "꿈이 없어서 고민이에요. 어떻게 찾을 수 있을까요?",
    "무언가를 시작하는 게 두려워요. 어떻게 극복할 수 있을까요?",
    "실패가 두려워서 도전하지 못하고 있어요.",
    "나이는 계속 먹는데, 아직도 내 자리를 못 찾았어요.",
    "다른 사람들과 비교하는 게 힘들어요.",
    "내 삶이 의미 없는 것처럼 느껴질 때 어떻게 해야 할까요?",
    "늘 똑같은 일상이 반복되는데, 이대로 괜찮을까요?",
    "미래가 불안할 때 마음을 다스리는 법이 있을까요?",

    # 🔹 감정 & 내면 고민
    "내 감정을 컨트롤하는 게 어려워요.",
    "늘 우울하고 무기력한데, 어떻게 해야 할까요?",
    "나 자신을 사랑하는 방법을 알고 싶어요.",
    "자존감이 낮아서 힘들어요.",
    "늘 죄책감을 느끼며 살아가고 있어요.",
    "혼자 있는 시간이 너무 외롭게 느껴져요.",
    "사람들 앞에서 나를 숨기고 사는 것 같아요.",
    "완벽해야 한다는 부담감에서 벗어나고 싶어요.",
    "늘 다른 사람들에게 맞추며 사는 게 지쳐요.",
    "마음의 평화를 찾는 방법이 있을까요?",

    # 🔹 일 & 돈 고민
    "지금 하는 일이 나에게 맞지 않는 것 같아요.",
    "내가 하고 싶은 일과 현실 사이에서 고민돼요.",
    "돈 걱정 없이 사는 방법이 있을까요?",
    "노력해도 성과가 없을 때 어떻게 해야 할까요?",
    "직장에서 인정받지 못하는 기분이에요.",
    "퇴사하고 싶지만, 현실적으로 어려워요.",
    "일과 삶의 균형을 어떻게 맞출 수 있을까요?",
    "돈을 벌기 위해 하기 싫은 일을 해야 할까요?",
    "경제적 불안감을 극복하는 방법이 있을까요?",
    "내가 하고 싶은 일로 먹고 살 수 있을까요?",

    # 🔹 외로움 & 인간관계 공허함
    "외로움을 극복하는 방법이 있을까요?",
    "아무도 나를 이해해 주지 않는 것 같아요.",
    "관계에서 오는 상처가 반복될 때 어떻게 해야 할까요?",
    "누군가에게 의지하고 싶은데, 방법을 모르겠어요.",
    "내 이야기를 진심으로 들어주는 사람이 없어요.",
    "사람들에게 상처받지 않고 사는 방법이 있을까요?",
    "다들 행복해 보이는데, 나만 그런 게 아닌 것 같아요.",
    "혼자 있는 시간을 즐길 수 있는 방법이 있을까요?",
    "늘 남들에게 맞춰주는 관계가 힘들어요.",
    "누군가에게 진짜 내 마음을 표현하는 게 어려워요."
]

# ✅ 현재 표시할 질문 리스트 (9개씩 랜덤 출력)
if "question_list" not in st.session_state or not st.session_state.question_list:
    st.session_state.question_list = random.sample(question_pool, 9)


# ✅ 채팅 UI 출력 (이전 대화 유지)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user", avatar=USER_AVATAR).write(f"**[{USER_NICKNAME}]** {msg['content']}")
    else:
        st.chat_message("assistant", avatar=AI_AVATAR).write(f"**[한줄성경]** {msg['content']}")



# ✅ 자연어 입력 필드 추가
st.subheader("📌 신앙과 삶의 고민이 있다면, 마음을 나누어 보세요.")


user_input = st.text_input("질문을 입력하세요:", placeholder="예: 하나님을 신뢰하는 법을 알고 싶어요.")

# ✅ 버튼 클릭 시 자동 입력 + 질문 변경
selected_question = None
# ✅ 3열 배치 (총 9개 질문 버튼)
cols = st.columns(3)  
for i, q in enumerate(st.session_state.question_list):
    with cols[i % 3]:  
        if st.button(q, use_container_width=True):
            selected_question = q

# ✅ 질문 선택 또는 자연어 입력 시 응답 시작
if selected_question or user_input:
    user_query = selected_question if selected_question else user_input
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user", avatar=USER_AVATAR).write(f"**[{USER_NICKNAME}]** {user_query}")

    # ✅ AI 응답 스트리밍 시작 (이전 대화 삭제 없이 유지)
    with st.chat_message("assistant", avatar=AI_AVATAR):
        st.write_stream(stream_bible_response(user_query))

    # ✅ 새로운 질문 리스트 업데이트 (이전 대화 삭제 없음)
    st.session_state.question_list = random.sample(question_pool, 9)

# ✅ 후속 질문 실행 (사용자가 버튼을 눌렀을 경우)
if st.session_state.follow_up:
    with st.chat_message("assistant", avatar=AI_AVATAR):
        st.write_stream(stream_follow_up_response(st.session_state.follow_up))


