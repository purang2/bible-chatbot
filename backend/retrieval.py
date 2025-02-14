import json
import re

# 성경 책 이름 매핑 (축약 형태 변환)
bible_book_map = {
    "창세기": "창", "출애굽기": "출", "레위기": "레", "민수기": "민", "신명기": "신",
    "여호수아": "수", "사사기": "삿", "룻기": "룻", "사무엘상": "삼상", "사무엘하": "삼하",
    "열왕기상": "왕상", "열왕기하": "왕하", "역대상": "대상", "역대하": "대하",
    "에스라": "스", "느헤미야": "느", "에스더": "에", "욥기": "욥", "시편": "시",
    "잠언": "잠", "전도서": "전", "아가": "아", "이사야": "사", "예레미야": "렘",
    "예레미야애가": "애", "에스겔": "겔", "다니엘": "단", "호세아": "호", "요엘": "욜",
    "아모스": "암", "오바댜": "옵", "요나": "욘", "미가": "미", "나훔": "나",
    "하박국": "합", "스바냐": "습", "학개": "학", "스가랴": "슥", "말라기": "말",
    "마태복음": "마", "마가복음": "막", "누가복음": "눅", "요한복음": "요",
    "사도행전": "행", "로마서": "롬", "고린도전서": "고전", "고린도후서": "고후",
    "갈라디아서": "갈", "에베소서": "엡", "빌립보서": "빌", "골로새서": "골",
    "데살로니가전서": "살전", "데살로니가후서": "살후", "디모데전서": "딤전",
    "디모데후서": "딤후", "디도서": "딛", "빌레몬서": "몬", "히브리서": "히",
    "야고보서": "약", "베드로전서": "벧전", "베드로후서": "벧후", "요한일서": "요일",
    "요한이서": "요이", "요한삼서": "요삼", "유다서": "유", "요한계시록": "계"
}

# 성경 JSON 데이터 로드
def load_bible_json():
    with open("data/bible.json", "r", encoding="utf-8") as f:
        return json.load(f)

bible_data = load_bible_json()

# ✅ 성경 구절을 JSON 키 형식으로 변환하는 함수
def format_bible_reference(reference):
    match = re.match(r"([가-힣]+)\s?(\d+):(\d+)", reference)
    if match:
        book, chapter, verse = match.groups()
        short_book = bible_book_map.get(book, book)  # 축약된 책 이름 찾기
        return f"{short_book}{chapter}:{verse}"
    return reference

# ✅ JSON에서 성경 구절 검색
def get_bible_verse(reference):
    formatted_ref = format_bible_reference(reference)
    return bible_data.get(formatted_ref, "(해당 번역을 찾을 수 없음)")

def replace_bible_references(text):
    """더 강건한 성경 구절 대체 함수"""
    
    # 더 유연한 패턴
    pattern = r'\((\d+)\)\s*([가-힣]+)\s*(\d+):(\d+)(?:-\d+)?(?:\s*[-–]\s*["\']([^"\']+)["\'])*'
    
    def replacement(match):
        try:
            index = match.group(1)
            book = match.group(2)
            chapter = match.group(3)
            verse = match.group(4)
            
            # 책 이름 정규화
            normalized_book = None
            for full_name, short_name in bible_book_map.items():
                if book in [full_name, short_name]:
                    normalized_book = full_name
                    break
            
            if not normalized_book:
                print(f"Warning: Unknown book name '{book}'")
                return match.group(0)
            
            # 정확한 성경 구절 가져오기
            formatted_ref = format_bible_reference(f"{normalized_book} {chapter}:{verse}")
            correct_translation = get_bible_verse(formatted_ref)
            
            if correct_translation != "(해당 번역을 찾을 수 없음)":
                # 하나의 깔끔한 형식으로 반환
                return f'({index}) {normalized_book} {chapter}:{verse} - "{correct_translation}"'
            else:
                print(f"Warning: Cannot find translation for {formatted_ref}")
                return match.group(0)
                
        except Exception as e:
            print(f"Error processing verse: {str(e)}")
            return match.group(0)
    
    # 먼저 [추천 성경구절] 태그 처리
    parts = text.split("[추천 성경구절]")
    if len(parts) > 1:
        main_text = parts[0]
        verses_text = parts[1]
        
        # 성경 구절 부분만 처리
        processed_verses = re.sub(pattern, replacement, verses_text)
        
        # 다시 합치기
        return f"{main_text}[추천 성경구절]{processed_verses}"
    
    # [추천 성경구절] 태그가 없는 경우 전체 텍스트에서 처리
    return re.sub(pattern, replacement, text)




def get_verse_context(book, chapter, verse):
    """성경 구절 컨텍스트를 가져오는 메인 함수"""
    try:
        # 전후 구절 가져오기 (예: 현재 구절 기준 앞뒤 2절씩)
        context = get_verse_range(book, chapter, int(verse), 2)
        return context, 200
    except Exception as e:
        print(f"Error getting verse context: {str(e)}")
        return {"error": str(e)}, 500

def get_verse_range(book, chapter, verse, range_size=2):
    """성경 구절의 전후 문맥을 가져오는 함수"""
    try:
        # 책 이름을 축약형으로 변환 (예: 빌립보서 -> 빌)
        book_short = None
        for full_name, short_name in bible_book_map.items():
            if book in [full_name, short_name]:
                book_short = short_name
                break
        
        if not book_short:
            raise ValueError(f"Invalid book name: {book}")

        # 전후 범위 계산
        start_verse = max(1, verse - range_size)
        end_verse = verse + range_size
        
        results = []
        for v in range(start_verse, end_verse + 1):
            key = f"{book_short}{chapter}:{v}"
            if key in bible_data:
                results.append({
                    "verse_number": v,
                    "text": bible_data[key],
                    "is_target": v == verse
                })
        
        return {
            "book": book,
            "chapter": chapter,
            "verses": results
        }
    except Exception as e:
        print(f"Error in get_verse_range: {str(e)}")
        raise



def extract_bible_references(text):
    """
    LLM 응답에서 성경 구절을 추출하는 강건한 함수
    
    고려사항:
    1. 다양한 구분자 패턴 (-, –, ～, ~, :, ：등)
    2. 따옴표 변형 (", ", ', ', ˮ, ˮ 등)
    3. 공백 불일치
    4. 줄바꿈 변형
    5. 누락된 정보 복구
    6. 중복 제거
    """
    
    def clean_text(text):
        """텍스트 전처리 및 정규화"""
        # 일반적인 따옴표로 정규화
        quote_chars = r'[""''ˮˮ`´]'
        text = re.sub(quote_chars, '"', text)
        
        # 구분자 정규화
        separator_chars = r'[–—―∼〜~─━]'
        text = re.sub(separator_chars, '-', text)
        
        # 공백 정규화
        text = re.sub(r'\s+', ' ', text)
        
        # 콜론 정규화
        text = re.sub(r'[：:］］]', ':', text)
        
        return text.strip()

    def is_valid_verse(verse):
        """성경 구절 유효성 검사"""
        required_fields = ['index', 'reference', 'text']
        if not all(field in verse for field in required_fields):
            return False
        if not all(verse[field].strip() for field in required_fields):
            return False
        # 참조 형식 검증
        if not re.match(r'^[가-힣]+\s*\d+:\d+(?:-\d+)?$', verse['reference']):
            return False
        return True

    def normalize_verse(verse):
        """성경 구절 정보 정규화"""
        if not verse:
            return None
            
        # 인덱스 정규화
        try:
            verse['index'] = str(int(verse['index']))  # 숫자만 추출
        except (ValueError, TypeError):
            return None
            
        # 참조 정규화
        verse['reference'] = re.sub(r'\s+', ' ', verse['reference']).strip()
        
        # 본문 정규화
        verse['text'] = verse['text'].strip()
        
        return verse if is_valid_verse(verse) else None

    try:
        # 텍스트 전처리
        cleaned_text = clean_text(text)
        
        # 메인 메시지와 성경 구절 영역 분리
        main_parts = re.split(r'\[추천\s*성경\s*구절\]|\[성경\s*구절\]|\[구절\]', cleaned_text, maxsplit=1)
        main_message = main_parts[0].strip()
        verses_text = main_parts[1] if len(main_parts) > 1 else cleaned_text
        
        # 성경 구절 패턴 (더 유연한 버전)
        patterns = [
            # 기본 패턴
            r'\((\d+)\)\s*([가-힣]+\s*\d+:\d+(?:-\d+)?)\s*[-―~]\s*["\']([^"\']+)["\']',
            # 괄호나 따옴표가 누락된 경우
            r'(?:\()?(\d+)(?:\))?\s*([가-힣]+\s*\d+:\d+(?:-\d+)?)\s*[-―~]\s*([^"\'\n]+?)(?=\s*(?:\(\d+\)|$))',
            # 구분자가 누락된 경우
            r'\((\d+)\)\s*([가-힣]+\s*\d+:\d+(?:-\d+)?)\s*["\']([^"\']+)["\']',
        ]
        
        verses = []
        seen_references = set()  # 중복 체크를 위한 집합
        
        # 각 패턴으로 시도
        for pattern in patterns:
            matches = re.finditer(pattern, verses_text)
            for match in matches:
                try:
                    verse = {
                        'index': match.group(1),
                        'reference': match.group(2),
                        'text': match.group(3)
                    }
                    
                    # 정규화 및 유효성 검사
                    normalized_verse = normalize_verse(verse)
                    if normalized_verse:
                        # 중복 체크
                        ref_key = f"{normalized_verse['reference']}:{normalized_verse['text']}"
                        if ref_key not in seen_references:
                            verses.append(normalized_verse)
                            seen_references.add(ref_key)
                            
                except (IndexError, AttributeError):
                    continue
        
        # 인덱스 순서대로 정렬
        verses.sort(key=lambda x: int(x['index']))
        
        # 최소한 하나의 성경 구절이 필요
        if not verses:
            print("Warning: No valid bible verses found in the text")
        
        return {
            'main_message': main_message,
            'verses': verses
        }
        
    except Exception as e:
        print(f"Error processing bible references: {str(e)}")
        return {
            'main_message': text,
            'verses': []
        }