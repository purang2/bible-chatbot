# Code of Conduct

## ■ 개요 및 목적
- AI 챗봇 형태 성경 구절 검색 사용자 경험 증대 목적의 ‘한줄성경’ 프로젝트.
- 개인적 고민, 중대한 선택 등에 적합한 성경 구절 답변 제공하는 감성적 AI 기술
- 종교 및 윤리적 고민 없는 신앙적 고민 상담 및 잠재적인 사회불안, 우울감 완화 효능의 양방향 챗봇

## ■ 기술적 측면 검토

#### 데이터셋 
- 본 프로젝트는 성경 데이터셋을 구축할 때, [개역개정 한글 성경 (KRV)] 포맷으로 JSON 파일로 수집한다. 성경의 분량은 번역 버전과 별개로 고정된 1,189장,31,102절이며, 각 절을 하나의 key-value쌍으로 하여 총 31,102개의 key-value 아이템을 가진 json을 사용. key는 “창 1:1” value는 “태초에 하나님이 천지를 창조하시니라”의 표준적인 형태로 변환하여 사용한다. 데이터셋 자체의 품질 우려가 발생하면 일부 샘플 랜덤 추출 후 수기 대조 검증 과정을 거쳐 검증

#### 데이터 전처리 
- 성경 데이터셋을 서비스 방향에 좀 더 부합하도록 최적화하고 사용자 경험을 개선하고자 데이터 전처리를 고려한다. 성경 데이터의 흥미로운 점은 성경말씀에서 유독 장과 절이 널리 알려진 구절들이 있고 공통적인 몇 가지 특징을 보인다. (핵심 교리를 담고 있는 내용, 짧고 강렬한 메시지형, 위로와 희망을 주는 내용, 예배와 기도에서 자주 사용 내용, 역사적으로 중요한 사건과 관련이 있는 내용)

#### 메타데이터 태깅 시스템
- 성경에는 유독 알려진 장과 절이 있다는 특성상, 메타데이터 태깅 후 성경 구절과 질문 사이의 메타데이터 매핑으로 로직 처리 시 단순 성경DB 컨텍스트 활용에 비해 성능이 매끄러워 질 것으로 가설을 세울 수 있는데, 이를 구현하기 위한 방법론으로 자연어 처리 시퀀스 레이블링 기술을 응용하여 성경구절DB 사전 태깅, 사용자 질문 실시간 태깅 후 태깅 매칭도가 높은 성경구절을 답변에 활용한다.
- 태깅 시스템 설계는 다음을 고려 중이다: 감정 기반 태깅 (위로,평안,인내 등), 상황 기반 태깅 (슬픔을 겪을 때, 결정을 내려야 할 때 등), 주제 기반 태깅 (구원, 믿음, 기도 등). 다방면으로 테스트 후 가장 적합한 방식으로로 최적화한다.
  > 성경 구절 → 주제/감성 → Embedding 단계 사전 레이블링> 예) “불안” 태그 → 관련된 시편, 요한복음 구절 등을 사전에 한 번에 관리
  

#### RAG 시스템
- 상업형 LLM (ChatGPT 등)은 성경구절의 일부를 간혹 틀리게 답변한다. 정확한 성경구절을 출력하기 위해 LLM 할루시네이션을 방지해야 한다. RAG 시스템 구축은 LangChain 기반 Retriever, VectorSpace, Reranker를 구축하여 DB를 연동하고. RAG 프롬프트 구조 설계는 관련 최신 연구 동향을 참고하여 직접 설계 및 LangSmith를 통해 프롬프트 버전을 관리한다.


#### 답변 성능 품질 테스트
- LLM 파이프라인의 사실성(Faithfulness) 및 일관성 성능을 검증하기 위한 자체 테스트 케이스를 마련(예: 테스트 질문 100개 마련 → 토큰 단위 대조 실험) 해 성능을 테스트하고 결과를 수치화한다. (예시 - RAG 적용 전: 62.59%/ 적용 후: 99.67%). 최근 각광받는 Cache-Augmented Generation도 성능 고도화 필요시 추가 검토한다.


## ■ 분야 특성/주의사항 검토 

- 성경 / 온라인 성경에 대한 문화적 인식 필요 | 방안: 사회 속 종교인 다양한 자문, 문서 및 영상 자료 등 조사
- 사례: 성경 구절의 각기 다른 번역 > 성경은 각기 다르게 번역 되는 경향이 있음.
  > 국내 주요 번역 - (1) 개역한글 (KRV) (2) 현대인의 성경 (KLB) (3) 새번역 (RNKSV). 동일한 복음서의 내용의 같은 구절도 다르게 번역될 수 있음. 이러한 문화를 반드시 이해하고 개발에 착수하는 것이 진정성 면에서 중요



