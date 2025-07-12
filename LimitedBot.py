import os
import time
import logging
from collections import defaultdict
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# API 설정 - Pro 계정 키 사용
GOOGLE_API_KEY = "AIzaSyCmH1flv0HSRp8xYa1Y8oL7xnpyyQVuIw8"  # Gemini Pro 계정 API 키
TELEGRAM_BOT_TOKEN = "8064422632:AAFkFqQDA_35OCa5-BFxeHPA9_hil4cY8Rg"
MODEL_NAME = "gemini-2.5-pro"  # 최신 Pro 모델 사용

# Gemini 설정
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# 사용자별 사용량 추적
user_usage = defaultdict(lambda: {"daily": 0, "last_reset": time.time()})

# 사용 제한 설정
LIMITS = {
    "daily_per_user": 50,  # 사용자당 하루 50개
    "vip_daily": 200,      # VIP 사용자는 200개
    "admin_daily": 1000,   # 관리자는 1000개
}

# VIP 사용자 목록 (사용자 ID 또는 username)
VIP_USERS = []  # 친구들 ID 추가
ADMIN_USERS = []  # 관리자 ID 추가

def get_user_limit(user_id):
    """사용자별 제한량 반환"""
    if user_id in ADMIN_USERS:
        return LIMITS["admin_daily"]
    elif user_id in VIP_USERS:
        return LIMITS["vip_daily"]
    else:
        return LIMITS["daily_per_user"]

def check_user_limit(user_id):
    """사용자 제한 확인"""
    current_time = time.time()
    user_data = user_usage[user_id]
    
    # 24시간 지났으면 리셋
    if current_time - user_data["last_reset"] > 86400:  # 24시간
        user_data["daily"] = 0
        user_data["last_reset"] = current_time
    
    # 제한 확인
    limit = get_user_limit(user_id)
    if user_data["daily"] >= limit:
        return False, limit, user_data["daily"]
    
    # 사용량 증가
    user_data["daily"] += 1
    return True, limit, user_data["daily"]

async def chat_with_gemini_limited(text: str, user_id: int) -> str:
    """제한된 Gemini 채팅"""
    try:
        # 사용 제한 확인
        can_use, limit, current_usage = check_user_limit(user_id)
        
        if not can_use:
            return f"😅 일일 사용 제한에 도달했습니다!\n" \
                   f"📊 사용량: {current_usage}/{limit}\n" \
                   f"🕐 내일 다시 이용해주세요!"
        
        # Gemini 호출
        response = model.generate_content(text)
        
        # 사용 통계 로깅
        logger.info(f"사용자 {user_id} - 사용량: {current_usage}/{limit}")
        
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini API 오류: {e}")
        return "죄송합니다. 잠시 후 다시 시도해주세요. 😅"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """봇 시작 메시지"""
    user_id = update.effective_user.id
    user_limit = get_user_limit(user_id)
    
    await update.message.reply_text(
        f'🎉 사용량 제한 Gemini AI 봇입니다!\n'
        f'📊 일일 사용 제한: {user_limit}개\n'
        f'💡 /status 명령어로 사용량을 확인하세요!'
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """사용량 확인"""
    user_id = update.effective_user.id
    user_data = user_usage[user_id]
    limit = get_user_limit(user_id)
    
    # 리셋 시간 계산
    reset_time = user_data["last_reset"] + 86400
    hours_left = max(0, (reset_time - time.time()) / 3600)
    
    status_text = f"📊 **사용량 현황**\n\n" \
                  f"🔢 오늘 사용량: {user_data['daily']}/{limit}\n" \
                  f"⏰ 리셋까지: {hours_left:.1f}시간\n" \
                  f"🎯 사용자 등급: {'관리자' if user_id in ADMIN_USERS else 'VIP' if user_id in VIP_USERS else '일반'}"
    
    await update.message.reply_text(status_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """메시지 처리"""
    user_message = update.message.text
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    logger.info(f"사용자 {user_name} ({user_id}): {user_message}")
    
    # "생각 중..." 메시지
    thinking_message = await update.message.reply_text("🤔 생각 중...")
    
    # 제한된 Gemini 호출
    response = await chat_with_gemini_limited(user_message, user_id)
    
    # 응답 전송
    await thinking_message.delete()
    await update.message.reply_text(response)

def main() -> None:
    """봇 시작"""
    logger.info("🚀 사용량 제한 봇 시작!")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # 핸들러 등록
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 봇 실행
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 