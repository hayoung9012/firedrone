from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

# SQLAlchemy 설정
engine = None
SessionLocal = None
Base = declarative_base()

def get_engine():
    global engine
    if engine is None:
        engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
    return engine

def get_session_local():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return SessionLocal


# 데이터베이스 모델
class SensorReading(Base):
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    gas = Column(Float, nullable=False)  # MQ-2 가스 센서 (ppm)
    temp = Column(Float, nullable=False)  # IR 온도 센서 (°C)
    altitude = Column(Float, nullable=False)  # LiDAR 고도 센서 (m)


class FireAlert(Base):
    __tablename__ = "fire_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    conditions = Column(String, nullable=False)  # "3개 조건 충족" 등
    gas = Column(Float, nullable=False)
    ir = Column(Float, nullable=False)
    yolo = Column(Boolean, nullable=False)
    action = Column(String, nullable=False)  # "자동 투하" 또는 "수동 투하"
    lat = Column(Float, nullable=True)  # 위도 (옵션)
    lon = Column(Float, nullable=True)  # 경도 (옵션)


# 데이터베이스 초기화
def init_db():
    """테이블 생성"""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


# 의존성 주입용 함수
def get_db():
    session_local = get_session_local()
    db = session_local()
    try:
        yield db
    finally:
        db.close()

