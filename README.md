# 📌 Bible Chatbot

<div align="center">
 <p>
   <img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=React&logoColor=white"/>
   <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=Flask&logoColor=white"/>
   <img src="https://img.shields.io/badge/GPT--4o-mini-412991?style=flat&logo=OpenAI&logoColor=white"/>
 </p>
</div>

<div align="center">
 <img src="images/screen2.png" width="210px" style="margin: 0 10px" />
 <img src="images/screen3.png" width="210px" style="margin: 0 10px" />
 <img src="images/screen4.png" width="210px" style="margin: 0 10px" />
 <img src="images/screen5.png" width="210px" style="margin: 0 10px" />
</div>

### 1. 환경 설정 (최초 1회)

```bash
# 프로젝트 클론 후 backend 디렉토리로 이동
git clone <repo-url>
cd bible-chatbot/backend

# 가상 환경 생성 및 활성화 (선택 사항)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# 필수 패키지 설치
pip install -r requirements.txt
```

### 2. 백엔드 실행

```bash
cd backend
python app.py
```

### 3. 프론트엔드 실행

```bash
cd ../frontend
npm install
npm start
```

### 4. 환경 변수 설정 (backend/.env)

백엔드 실행 전 `.env` 파일을 backend 폴더 내에 생성하고 아래처럼 설정합니다.

```ini
OPENAI_API_KEY=your-api-key-here
```

`.env` 파일은 `.gitignore`에 추가하여 레포지토리에 올리지 않도록 주의하세요.

### 5. 실행 확인

백엔드가 정상적으로 실행되면, Flask 서버가 `http://127.0.0.1:5000`에서 실행됩니다.

프론트엔드를 실행하면 `http://localhost:3000`에서 챗봇 UI를 확인할 수 있습니다.
