import os
import random
import time
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# 여러 Google API 키 설정 (각각 다른 모델 사용)
API_CONFIG = [
    {
        "api_key": "AIzaSyCmH1flv0HSRp8xYa1Y8oL7xnpyyQVuIw8",  # 본인 Pro 계정
        "model": "gemini-2.5-pro",  # Pro 모델
        "name": "Pro계정"
    },
    {
        "api_key": "AIzaSyDrHQu3h3NchjchCjOiCV533ygfW-Cz5AU",  # 친구 일반 계정
        "model": "gemini-1.5-flash",  # 일반 모델
        "name": "일반계정"
    }
    # 추가 API 키들을 여기에 추가하세요
    # {
    #     "api_key": "친구2_API_키",
    #     "model": "gemini-1.5-flash",
    #     "name": "친구2계정"
    # }
]

# 텔레그램 봇 토큰
BOT_TOKEN = "8064422632:AAFkFqQDA_35OCa5-BFxeHPA9_hil4cY8Rg"

# API 키 사용 통계
api_usage = {}
for config in API_CONFIG:
    api_usage[config["api_key"]] = {
        "requests": 0,
        "errors": 0,
        "last_used": 0,  # None을 0으로 변경
        "model": config["model"],
        "name": config["name"]
    }

def get_available_api_key():
    """사용 가능한 API 키 반환 (라운드 로빈 방식)"""
    current_time = time.time()
    
    # 1분 이내에 15번 미만 사용한 키 찾기
    for config in API_CONFIG:
        api_key = config["api_key"]
        if current_time - api_usage[api_key]["last_used"] > 60:
            # 1분 지났으면 카운트 리셋
            api_usage[api_key]["requests"] = 0
        
        if api_usage[api_key]["requests"] < 15:
            api_usage[api_key]["requests"] += 1
            api_usage[api_key]["last_used"] = current_time
            return config  # 전체 config 반환
    
    # 모든 키가 제한에 걸렸으면 가장 오래된 키 사용
    oldest_config = min(API_CONFIG, key=lambda c: api_usage[c["api_key"]]["last_used"])
    api_usage[oldest_config["api_key"]]["requests"] = 1
    api_usage[oldest_config["api_key"]]["last_used"] = current_time
    return oldest_config

async def call_gemini_api(message: str):
    """Gemini API 호출 (로드 밸런싱 적용)"""
    try:
        # 사용 가능한 API 키 가져오기
        config = get_available_api_key()
        api_key = config["api_key"]
        model_name = config["model"]
        account_name = config["name"]
        
        # 해당 키로 Gemini 설정
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # 요청 보내기
        response = model.generate_content(message)
        
        # 성공 로그
        logger.info(f"✅ {account_name} ({model_name}) 사용 성공")
        
        return response.text
        
    except Exception as e:
        # 에러 카운트 증가
        api_usage[api_key]["errors"] += 1
        logger.error(f"❌ {account_name} ({model_name}) 에러: {e}")
        
        # 다른 키로 재시도
        if api_usage[api_key]["errors"] < 3:
            logger.info("🔄 다른 API 키로 재시도...")
            return await call_gemini_api(message)
        else:
            return f"죄송합니다. 일시적인 오류가 발생했습니다: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """봇 시작 메시지"""
    await update.message.reply_text(
        '🎉 다중 API 키 Gemini AI 봇입니다!\n'
        '👥 여러 명이 함께 사용할 수 있어요!\n'
        '⚡ 로드밸런싱으로 제한 없이 사용하세요!'
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """API 사용 현황 보기"""
    status_text = "📊 **API 사용 현황**\n\n"
    
    for i, config in enumerate(API_CONFIG):
        api_key = config["api_key"]
        usage = api_usage[api_key]
        account_name = config["name"]
        model_name = config["model"]
        
        # 마지막 사용 시간 계산
        if usage['last_used'] == 0:
            last_used_text = "사용 안함"
        else:
            minutes_ago = int((time.time() - usage['last_used']) / 60)
            if minutes_ago < 1:
                last_used_text = "방금 전"
            else:
                last_used_text = f"{minutes_ago}분 전"
        
        status_text += f"**{account_name}** ({model_name})\n"
        status_text += f"• 분당 사용: {usage['requests']}/15\n"
        status_text += f"• 에러 수: {usage['errors']}\n"
        status_text += f"• 마지막 사용: {last_used_text}\n\n"
    
    await update.message.reply_text(status_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """메시지 처리"""
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    logger.info(f"사용자 {user_name}: {user_message}")
    
    # "생각 중..." 메시지
    thinking_message = await update.message.reply_text("🤔 생각 중...")
    
    # 로드밸런싱된 Gemini 호출
    response = await call_gemini_api(user_message)
    
    # 응답 전송
    await thinking_message.delete()
    await update.message.reply_text(response)

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """번역 명령어"""
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("사용법: /translate [언어] [텍스트]")
            return
        
        target_language = args[0]
        text_to_translate = " ".join(args[1:])
        
        prompt = f"다음 텍스트를 {target_language}로 번역해주세요: {text_to_translate}"
        response = await call_gemini_api(prompt)
        
        await update.message.reply_text(f"🌍 번역 결과:\n{response}")
        
    except Exception as e:
        logger.error(f"번역 오류: {e}")
        await update.message.reply_text("번역 중 오류가 발생했습니다. 😅")

def main() -> None:
    """봇 시작"""
    logger.info(f"🚀 다중 API 키 봇 시작! (총 {len(API_CONFIG)}개 키 사용)")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 핸들러 등록
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("translate", translate_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 봇 실행
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 