import streamlit as st
from openai import OpenAI

# Streamlit 설정
st.set_page_config(page_title="Bible AI Chatbot", page_icon="📖")
st.title("📖 Bible AI Chatbot")
st.write("Receive Bible verses based on your concerns. (Supports Korean input)")

# OpenAI API 설정
client = OpenAI(api_key=st.secrets["chatgpt"])

# 사용자 입력 (한국어 가능)
user_input = st.text_input("🙏 당신의 질문을 입력하세요:", placeholder="예: 인내에 대한 성경 말씀은 무엇인가요?")

# 성경 구절 응답 생성 (현재는 GPT-4o가 자체적으로 제공)
def get_bible_response(query):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "너는 기독교 AI 챗봇이며, 성경 말씀을 정확하게 인용해야 한다.\n"
                "1. 성경 구절을 반드시 실제 존재하는 내용으로 제공하라.\n"
                "2. 구절을 재생성하지 말고, (책 이름 장:절) 형식으로 정확히 표기하라.\n"
                "3. 잘못된 출처를 제공하지 않도록 주의하며, 신뢰할 수 있는 내용만 전달하라.\n"
                "4. 인용된 구절이 너무 길면 일부만 제공하고 '...'을 사용하라.\n"
                "5. 사용자에게 공감하는 어조를 유지하되, 신학적 해설은 단순하고 명확하게 설명하라.\n"
                "6. 기독교적 존중을 담아 '성도님', '주님께서는...' 등의 표현을 활용하라.\n"
                "7. 출처가 명확하지 않을 경우, '시편 23편' 등의 일반적인 구절을 제안하라."
            )},
            {"role": "user", "content": f"질문: {query}"}
        ],
        max_tokens=700,
        temperature=0.65,
    )
    return response.choices[0].message.content.strip()

# 버튼 클릭 시 실행
if st.button("🔍 성경 구절 찾기"):
    if user_input:
        with st.spinner("📖 성경에서 답을 찾고 있습니다..."):
            explanation = get_bible_response(user_input)
            st.success("📖 성경 구절:")
            st.write("💬 **해설:**")
            st.write(explanation)
    else:
        st.warning("🙏 질문을 입력해주세요.")

# 푸터
st.markdown("---")
st.markdown("💡 *Powered by GPT-4o | Bible AI Chatbot*")
