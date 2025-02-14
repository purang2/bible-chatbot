# 성경 구절을 JSON 키 형식으로 변환하는 함수
def format_bible_reference(reference):
    match = re.match(r"([가-힣]+)\s?(\d+):(\d+)", reference)
    if match:
        book, chapter, verse = match.groups()
        short_book = bible_book_map.get(book, book)  # 축약된 책 이름 찾기
        return f"{short_book}{chapter}:{verse}"
    return reference

# JSON에서 성경 구절 검색
def get_bible_verse(reference):
    formatted_ref = format_bible_reference(reference)
    return bible_data.get(formatted_ref, "(해당 번역을 찾을 수 없음)")

# 성경 구절 자동 대체 함수
def replace_bible_references(text):
    for match in re.findall(r"[가-힣]+\s?\d+:\d+", text):
        formatted_ref = format_bible_reference(match)
        correct_translation = get_bible_verse(formatted_ref)
        if correct_translation != "(해당 번역을 찾을 수 없음)":
            text = text.replace(match, f"{match}: \"{correct_translation}\"")
    return text


def module1(user_query):
    # 8
    module1_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": PROMPT_1},
                {"role": "user", "content": user_query}
        ],
        max_tokens=700,
        temperature=0.7
    )

    module1_response.choices[0].message.content = replace_bible_references(module1_response.choices[0].message.content.strip())
    
    return module1_response.choices[0].message.content.strip()

def module2(user_query):
   module2_response = client.chat.completions.create(
         model="gpt-4o-mini",
         messages=[
             {"role": "system", "content": PROMPT_2},
             {"role": "user", "content": user_query}
         ],
         max_tokens=700,
         temperature=0.7,
       stream=True
      )
   
   return module2_response
   

def stream_bible_response(user_query):
    # 8
    module1_response = module1(user_query)
    module2_response = module2(module1_response)
    response = module2_response
    
    full_response = ""  # 전체 응답 저장

    for chunk in response:
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                full_response += delta.content
                yield delta.content  # ✅ 한 줄씩 반환
                time.sleep(0.02)  # ✅ 응답 속도 조절

    
    # ✅ 카드 형태로 출력
    st.markdown(f"""
        <div class="chat-card">
            <p>{module1_response}</p>
        </div>
    """, unsafe_allow_html=True)
    # ✅ 응답 저장 (대화 내역 유지)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
