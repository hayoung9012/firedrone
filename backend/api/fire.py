from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db, FireAlert
from models import FireAlertData, FireAlertResponse, ManualAlertData, DropCommand, StatusResponse
from api.websocket import manager

router = APIRouter(prefix="/api", tags=["화재 감지"])


@router.post("/fire_alert", response_model=StatusResponse)
async def fire_alert(
    data: FireAlertData,
    db: Session = Depends(get_db)
):
    """
    화재 감지 알림 (3개 조건 충족)
    - DB에 로그 저장
    - WebSocket으로 프론트엔드에 알림 전송
    """
    try:
        # DB에 화재 알림 저장
        alert = FireAlert(
            conditions=data.conditions,
            gas=data.gas,
            ir=data.ir,
            yolo=data.yolo,
            action="자동 투하",
            lat=data.lat,
            lon=data.lon
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        
        # WebSocket으로 알림 전송
        await manager.broadcast({
            "type": "fire_alert",
            "message": f"🔥 화재 발생 감지! 가스: {data.gas}ppm, IR: {data.ir}°C, YOLO: {'감지' if data.yolo else '미감지'}",
            "data": {
                "conditions": data.conditions,
                "gas": data.gas,
                "ir": data.ir,
                "yolo": data.yolo,
                "action": "자동 투하"
            }
        })
        
        return StatusResponse(ok=True, message="화재 알림 전송 완료")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"알림 전송 실패: {str(e)}")


@router.post("/manual_alert", response_model=StatusResponse)
async def manual_alert(
    data: ManualAlertData
):
    """
    수동 투하 알림 (2개 조건 충족)
    - WebSocket으로 프론트엔드에 확인 요청
    """
    try:
        await manager.broadcast({
            "type": "manual_alert",
            "message": f"🔥 {data.condition_count}개 조건 충족 — 수동 투하하시겠습니까?",
            "data": {
                "condition_count": data.condition_count
            }
        })
        
        return StatusResponse(ok=True, message="수동 알림 전송 완료")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"알림 전송 실패: {str(e)}")


@router.post("/drop", response_model=StatusResponse)
async def drop_command(
    command: DropCommand,
    db: Session = Depends(get_db)
):
    """
    투하 명령 (프론트엔드에서 사용자 확인 후 호출)
    - 젯슨으로 투하 명령 전송
    - DB에 수동 투하 로그 저장
    """
    if not command.confirmed:
        raise HTTPException(status_code=400, detail="투하가 확인되지 않았습니다")
    
    try:
        # TODO: 여기에 젯슨으로 실제 투하 명령 전송 로직 추가
        # 예: requests.post("http://jetson-ip:PORT/drop")
        
        # DB에 수동 투하 로그 저장
        alert = FireAlert(
            conditions="2개 조건 충족 (수동)",
            gas=0.0,  # 실제 값은 이전 센서 데이터에서 가져와야 함
            ir=0.0,
            yolo=False,
            action="수동 투하"
        )
        db.add(alert)
        db.commit()
        
        return StatusResponse(ok=True, message="투하 명령 전송 완료")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"투하 명령 실패: {str(e)}")


@router.get("/fire_log", response_model=List[FireAlertResponse])
async def get_fire_log(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    화재 경보 로그 조회
    """
    alerts = db.query(FireAlert).order_by(FireAlert.ts.desc()).limit(limit).all()
    return alerts

