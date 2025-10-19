from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from database import init_db
from api import sensor, fire
from api.websocket import websocket_endpoint

# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Fire Drone 모니터링 시스템 백엔드 API"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(sensor.router)
app.include_router(fire.router)


# WebSocket 엔드포인트
@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)


# 시작 이벤트
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행"""
    print(f"🚀 {settings.APP_NAME} v{settings.VERSION} 시작")
    print(f"📡 서버 주소: http://{settings.HOST}:{settings.PORT}")
    
    # PostgreSQL 비밀번호 입력받기
    if not settings.POSTGRES_PASSWORD:
        settings.POSTGRES_PASSWORD = input("PostgreSQL 비밀번호를 입력하세요: ")
    
    # 데이터베이스 테이블 생성
    try:
        init_db()
        print("✅ 데이터베이스 초기화 완료")
    except Exception as e:
        print(f"⚠️ 데이터베이스 초기화 실패: {e}")
        print("   PostgreSQL이 실행 중인지 확인하세요.")


# 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 실행"""
    print("🛑 서버 종료")


# 헬스 체크
@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# 서버 실행
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,  # 개발 모드: 코드 변경 시 자동 재시작
        log_level="info"
    )

