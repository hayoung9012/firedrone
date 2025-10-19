from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# 센서 데이터 모델
class SensorData(BaseModel):
    gas: float = Field(..., description="MQ-2 가스 센서 값 (ppm)", ge=0)
    temp: float = Field(..., description="IR 온도 센서 값 (°C)")
    altitude: float = Field(..., description="LiDAR 고도 센서 값 (m)", ge=0)
    lat: Optional[float] = Field(None, description="위도")
    lon: Optional[float] = Field(None, description="경도")


class SensorResponse(BaseModel):
    ts: datetime
    gas: float
    temp: float
    altitude: float
    
    class Config:
        from_attributes = True


# 화재 알림 모델
class FireAlertData(BaseModel):
    gas: float
    ir: float
    yolo: bool
    conditions: str = "3개 조건 충족"
    lat: Optional[float] = None
    lon: Optional[float] = None


class FireAlertResponse(BaseModel):
    id: int
    ts: datetime
    conditions: str
    gas: float
    ir: float
    yolo: bool
    action: str
    lat: Optional[float]
    lon: Optional[float]
    
    class Config:
        from_attributes = True


# 수동 알림 모델
class ManualAlertData(BaseModel):
    condition_count: int = Field(..., ge=1, le=3)


# 투하 명령 모델
class DropCommand(BaseModel):
    confirmed: bool = True
    reason: str = "화재 감지"


# API 응답 모델
class StatusResponse(BaseModel):
    ok: bool
    message: str = "성공"


# WebSocket 메시지 모델
class WSMessage(BaseModel):
    type: str  # "fire_alert", "manual_alert", "sensor_update"
    message: str
    data: Optional[dict] = None

