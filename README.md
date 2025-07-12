# 🤖 24/7 AI 텔레그램 봇 배포 가이드

컴퓨터를 끄지 않고도 24시간 돌아가는 AI 봇을 만들어보세요!

## 🎯 목표
- ✅ 24/7 무중단 서비스
- ✅ 완전 무료 호스팅
- ✅ Google Gemini AI 연동
- ✅ 쉬운 배포 (클릭 몇 번이면 끝!)

## 🚀 배포 방법들

### 1. 🌟 Railway (추천 - 가장 쉬움)

#### 장점:
- 완전 무료 (월 $5 크레딧)
- GitHub 연결만 하면 자동 배포
- 환경변수 설정 쉬움
- 로그 확인 가능

#### 단계:
1. **GitHub 저장소 만들기**
   - 이 폴더를 GitHub에 업로드
   
2. **Railway 가입**
   - https://railway.app 접속
   - GitHub 계정으로 로그인
   
3. **프로젝트 생성**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 업로드한 저장소 선택
   
4. **환경변수 설정**
   - 프로젝트 → Settings → Variables
   - 다음 변수들 추가:
     ```
     TELEGRAM_BOT_TOKEN = your_telegram_bot_token
     GOOGLE_API_KEY = your_google_api_key
     ```
   
5. **배포 완료!**
   - 자동으로 배포되고 24/7 실행됨

### 2. 🔥 Render (무료 대안)

#### 장점:
- 무료 플랜 750시간/월
- 자동 SSL 인증서
- 쉬운 배포

#### 단계:
1. **Render 가입**
   - https://render.com 접속
   - GitHub 계정으로 로그인
   
2. **Web Service 생성**
   - "New +" → "Web Service"
   - GitHub 저장소 연결
   
3. **설정**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python SimpleBot.py`
   
4. **환경변수 설정**
   - Environment Variables에 추가:
     ```
     TELEGRAM_BOT_TOKEN = your_telegram_bot_token
     GOOGLE_API_KEY = your_google_api_key
     ```

### 3. 🏠 라즈베리파이 (집에서 24/7)

#### 장점:
- 한 번 사면 평생 무료
- 전력 소모 적음 (월 전기료 약 1,000원)
- 완전한 통제 가능

#### 필요한 것:
- 라즈베리파이 4 (약 7만원)
- SD 카드 (약 1만원)
- 전원 어댑터

## 🔑 필요한 API 키들

### 1. 텔레그램 봇 토큰
1. @BotFather에게 메시지 보내기
2. `/newbot` 명령어 입력
3. 봇 이름 설정
4. 토큰 받기

### 2. Google Gemini API 키
1. https://aistudio.google.com/app/apikey 접속
2. "Create API Key" 클릭
3. 키 복사

## 💰 비용 비교

| 방법 | 비용 | 장점 | 단점 |
|------|------|------|------|
| Railway | 무료 ($5/월) | 가장 쉬움 | 크레딧 제한 |
| Render | 무료 (750시간) | 안정적 | 시간 제한 |
| 라즈베리파이 | 초기 8만원 | 완전 무료 | 초기 설정 복잡 |
| VPS | 월 $4-5 | 완전 통제 | 서버 관리 필요 |

## 🛠️ 파일 구조

```
TelegramBot/
├── SimpleBot.py          # 메인 봇 코드
├── requirements.txt      # 필요한 라이브러리
├── runtime.txt          # Python 버전
├── GeminiBot.py         # Gemini API 테스트 코드
├── TelegramBot.py       # OpenAI API 코드
└── README.md            # 이 파일
```

## 🚀 봇 기능들

### 📝 기본 기능
- 일반 채팅 (Gemini AI 응답)
- `/start` - 봇 시작
- `/help` - 도움말

### 🌟 특별 기능
- `/translate [언어] [텍스트]` - 번역
- `/code [설명]` - 코드 생성
- `/poem [주제]` - 시 창작

### 💡 예시
```
/translate 영어 안녕하세요
→ Hello

/code 리스트 정렬 함수
→ Python 코드 생성

/poem 겨울 눈
→ 겨울 눈에 대한 시 창작
```

## 🔧 로컬 테스트

```bash
# 라이브러리 설치
pip install -r requirements.txt

# 환경변수 설정 (Windows)
set TELEGRAM_BOT_TOKEN=your_token
set GOOGLE_API_KEY=your_key

# 봇 실행
python SimpleBot.py
```

## 🎉 배포 후 확인사항

1. **봇이 응답하는지 확인**
   - 텔레그램에서 `/start` 명령어 테스트
   
2. **로그 확인**
   - Railway/Render 대시보드에서 로그 확인
   
3. **24/7 작동 확인**
   - 몇 시간 후에도 봇이 응답하는지 확인

## 🆘 문제 해결

### 봇이 응답하지 않을 때:
1. API 키 확인
2. 환경변수 설정 확인
3. 로그에서 오류 메시지 확인

### 배포 실패 시:
1. requirements.txt 확인
2. Python 버전 확인 (3.9 이상)
3. 코드 문법 오류 확인

## 📞 지원

질문이 있으시면 언제든지 문의하세요!

---

🎯 **이제 당신의 AI 봇이 24/7 전 세계 어디서든 사용자들과 대화할 수 있습니다!** 🚀 