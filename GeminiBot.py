import google.generativeai as genai
import os
from pathlib import Path

# Google Gemini API 설정
# 방법 1: 환경변수 사용 (권장)
# genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# 방법 2: 직접 API 키 입력 (테스트용)
genai.configure(api_key="AIzaSyCmH1flv0HSRp8xYa1Y8oL7xnpyyQVuIw8")  # Gemini Pro 계정 API 키

# 사용 가능한 모델 확인
def list_models():
    """사용 가능한 Gemini 모델들 보기"""
    print("=== 사용 가능한 Gemini 모델들 ===")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
            print(f"  설명: {model.description}")
            print(f"  입력 토큰 제한: {model.input_token_limit}")
            print(f"  출력 토큰 제한: {model.output_token_limit}")
            print()

# 1. 기본 텍스트 생성 (채팅) - 이제 gemini-2.5-pro 사용!
def chat_with_gemini(message, model_name="gemini-2.5-pro"):
    """Gemini와 대화하기 - 최신 Pro 모델 사용!"""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        return f"에러: {e}"

# 2. 대화형 채팅 (대화 기록 유지) - 이제 gemini-2.5-pro 사용!
def start_chat_session(model_name="gemini-2.5-pro"):
    """대화 세션 시작"""
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=[])
    return chat

def chat_with_history(chat_session, message):
    """대화 기록을 유지하며 채팅"""
    try:
        response = chat_session.send_message(message)
        return response.text
    except Exception as e:
        return f"에러: {e}"

# 3. 이미지 분석 (Vision)
def analyze_image_gemini(image_path, question="이 이미지에 대해 설명해주세요"):
    """이미지 분석하기"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 이미지 파일 읽기
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        # 이미지와 텍스트를 함께 전송
        response = model.generate_content([question, {"mime_type": "image/jpeg", "data": image_data}])
        return response.text
    except Exception as e:
        return f"에러: {e}"

# 4. 코드 생성 및 설명
def generate_code_gemini(description):
    """코드 생성하기"""
    prompt = f"""
    다음 요구사항에 맞는 Python 코드를 작성해주세요:
    {description}
    
    코드만 작성하지 말고, 설명도 함께 해주세요.
    """
    return chat_with_gemini(prompt)

# 5. 문서 요약
def summarize_text_gemini(text):
    """텍스트 요약하기"""
    prompt = f"""
    다음 텍스트를 한국어로 간결하게 요약해주세요:
    
    {text}
    """
    return chat_with_gemini(prompt)

# 6. 번역
def translate_gemini(text, target_language="한국어"):
    """번역하기"""
    prompt = f"다음 텍스트를 {target_language}로 번역해주세요: {text}"
    return chat_with_gemini(prompt)

# 7. 창작 (시, 소설, 에세이 등)
def creative_writing_gemini(topic, style="에세이"):
    """창작하기"""
    prompt = f"{topic}에 대한 {style}를 작성해주세요. 창의적이고 흥미롭게 써주세요."
    return chat_with_gemini(prompt)

# 8. 수학 문제 풀이
def solve_math_gemini(problem):
    """수학 문제 풀기"""
    prompt = f"""
    다음 수학 문제를 단계별로 풀어주세요:
    {problem}
    
    풀이 과정을 자세히 설명해주세요.
    """
    return chat_with_gemini(prompt)

# 9. 언어 학습 도우미
def language_tutor_gemini(word_or_sentence, target_language="영어"):
    """언어 학습 도우미"""
    prompt = f"""
    "{word_or_sentence}"을/를 {target_language}로 번역하고, 
    다음 정보도 제공해주세요:
    1. 발음 (한글로)
    2. 문법 설명
    3. 예문 3개
    4. 유사한 표현들
    """
    return chat_with_gemini(prompt)

# 10. 스트리밍 응답 (실시간 답변)
def stream_response_gemini(message):
    """스트리밍으로 실시간 답변받기"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(message, stream=True)
        
        print("=== 실시간 답변 ===")
        full_response = ""
        for chunk in response:
            if chunk.text:
                print(chunk.text, end='', flush=True)
                full_response += chunk.text
        print("\n")
        return full_response
    except Exception as e:
        return f"에러: {e}"

# 사용 예시
if __name__ == "__main__":
    print("🤖 Google Gemini AI 봇 - 무료 버전!")
    print("=" * 50)
    
    # 모델 리스트 확인 (선택사항)
    # list_models()
    
    # 1. 기본 채팅 테스트
    print("\n1. 기본 채팅 테스트:")
    try:
        response = chat_with_gemini("안녕하세요! 오늘 날씨가 어때요?")
        print(response)
    except Exception as e:
        print(f"에러: {e}")
    
    # 2. 대화형 채팅 테스트
    print("\n2. 대화형 채팅 테스트:")
    try:
        chat = start_chat_session()
        response1 = chat_with_history(chat, "제 이름은 홍길동입니다.")
        print(f"응답1: {response1}")
        
        response2 = chat_with_history(chat, "제 이름이 뭐라고 했죠?")
        print(f"응답2: {response2}")
    except Exception as e:
        print(f"에러: {e}")
    
    # 3. 코드 생성 테스트
    print("\n3. 코드 생성 테스트:")
    try:
        code = generate_code_gemini("리스트에서 중복을 제거하는 함수")
        print(code)
    except Exception as e:
        print(f"에러: {e}")
    
    # 4. 번역 테스트
    print("\n4. 번역 테스트:")
    try:
        translation = translate_gemini("Hello, how are you today?")
        print(translation)
    except Exception as e:
        print(f"에러: {e}")
    
    # 5. 창작 테스트
    print("\n5. 창작 테스트:")
    try:
        creative = creative_writing_gemini("겨울 눈", "시")
        print(creative)
    except Exception as e:
        print(f"에러: {e}")
    
    # 6. 수학 문제 풀이
    print("\n6. 수학 문제 풀이:")
    try:
        math_solution = solve_math_gemini("2x + 5 = 15를 풀어주세요")
        print(math_solution)
    except Exception as e:
        print(f"에러: {e}")
    
    # 7. 스트리밍 응답 테스트
    print("\n7. 스트리밍 응답 테스트:")
    try:
        stream_response_gemini("인공지능의 미래에 대해 200자 정도로 설명해주세요")
    except Exception as e:
        print(f"에러: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 모든 테스트 완료!")
    print("💡 Google AI Studio에서 무료 API 키를 받으세요:")
    print("   https://aistudio.google.com/app/apikey") 