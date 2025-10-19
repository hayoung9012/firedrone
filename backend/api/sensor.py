from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta

from database import get_db, SensorReading
from models import SensorData, SensorResponse, StatusResponse
from config import settings

router = APIRouter(prefix="/api", tags=["센서"])


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """API 키 검증"""
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="유효하지 않은 API 키")
    return x_api_key


@router.post("/status", response_model=StatusResponse)
async def save_sensor_data(
    data: SensorData,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    젯슨에서 센서 데이터를 전송받아 DB에 저장
    """
    try:
        sensor_reading = SensorReading(
            gas=data.gas,
            temp=data.temp,
            altitude=data.altitude
        )
        db.add(sensor_reading)
        db.commit()
        db.refresh(sensor_reading)
        
        return StatusResponse(ok=True, message="데이터 저장 완료")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"저장 실패: {str(e)}")


@router.get("/status", response_model=SensorResponse)
async def get_latest_sensor_data(db: Session = Depends(get_db)):
    """
    최신 센서 데이터 1건 조회 (프론트엔드 폴링용)
    """
    latest = db.query(SensorReading).order_by(SensorReading.ts.desc()).first()
    
    if not latest:
        raise HTTPException(status_code=404, detail="데이터가 없습니다")
    
    return latest


@router.get("/sensor_log", response_model=List[SensorResponse])
async def get_sensor_log(
    limit: int = 50,
    from_time: Optional[datetime] = None,
    to_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    센서 데이터 히스토리 조회
    """
    query = db.query(SensorReading)
    
    if from_time:
        query = query.filter(SensorReading.ts >= from_time)
    if to_time:
        query = query.filter(SensorReading.ts <= to_time)
    
    # 최근 데이터부터 정렬
    results = query.order_by(SensorReading.ts.desc()).limit(limit).all()
    
    return results

