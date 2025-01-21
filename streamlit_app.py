import streamlit as st
from openai import OpenAI

# Streamlit 설정
st.set_page_config(page_title="Bible AI Chatbot", page_icon="📖")
st.title("📖 Bible AI Chatbot")
st.write("A chatbot that provides Bible verses with insights. (Supports Korean input)")

# OpenAI API 설정
client = OpenAI(api_key=st.secrets["chatgpt"])

# ✅ 대화 이력 저장 (채팅 UI를 위해 세션 상태 사용)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 성경 말씀을 찾아드리는 Bible AI Chatbot입니다. 무엇이든 물어보세요. 🙏"}
    ]

# ✅ 채팅 UI 출력 (이전 대화 표시)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ 사용자 입력 받기 (챗봇 입력 필드 사용)
if user_input := st.chat_input("✍️ 질문을 입력하세요 (예: 인내에 대한 성경 말씀은?)"):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ✅ AI 응답 생성 (스트리밍 지원)
    with st.chat_message("assistant"):
        with st.spinner("📖 성경에서 답을 찾고 있습니다..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": (
                "너는 기독교 AI 챗봇이며, 성경 말씀을 정확하게 인용해야 한다.\n"
                "1. 반드시 실제 존재하는 성경 구절의 개역성경 번역본만 반드시 제공하여 당신이 제시한 성경 구절이 구글에 검색시 한글자도 틀리지 않고 검색 결과에 개역성경 내용이 나와야만 하고, (책 이름 장:절) 형식으로 출처를 정확히 표기하라.\n"
                "2. 구절이 길 경우, 일부만 제공하고 '...'을 사용하되 출처는 명확히 표기하라.\n"
                "3. 사용자에게 공감하는 어조를 유지하며, 짧은 위로 문장을 추가하라. (예: '힘드셨겠네요.', '주님께서 함께 하십니다.')\n"
                "4. 기독교적 존중을 담아 '성도님', '주님께서는...' 등의 표현을 활용하라.\n"
                "5. 출처가 명확하지 않을 경우, 대표적인 구절(예: '시편 23편')을 추천하라."
            )},
                    *st.session_state.messages  # 기존 대화 내역 추가
                ],
                max_tokens=700,
                temperature=0.65,
                stream=True  # ✅ 스트리밍 응답 활성화
            )

            # ✅ 스트리밍 응답 출력 (점진적으로 표시)
            streamed_text = ""
            for no, chunk in enumerate(response, start=1):
                if chunk.choices and chunk.choices[0].delta.get("content"):
                    streamed_text += chunk.choices[0].delta["content"]
                    st.markdown(streamed_text)  # 실시간으로 업데이트

            # ✅ 최종 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": streamed_text})

# 푸터
st.markdown("---")
st.markdown("💡 *Powered by GPT-4o | Bible AI Chatbot*")
