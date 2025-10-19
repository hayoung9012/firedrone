# 🚁 Fire Drone 프로젝트

드론 화재 감지 모니터링 시스템 - 통합 저장소

## 📁 프로젝트 구조

```
firedrone/
├── backend/          # FastAPI 백엔드 서버
│   ├── api/         # API 엔드포인트
│   ├── main.py      # 서버 진입점
│   ├── database.py  # DB 모델
│   └── config.py    # 설정
├── frontend/        # HTML/CSS/JS 프론트엔드
│   ├── css/         # 스타일시트
│   ├── js/          # JavaScript
│   └── index.html   # 메인 페이지
└── README.md
```

## 🚀 빠른 시작

### 백엔드 실행

```bash
cd backend
pip install -r requirements.txt
python main.py
```

서버 주소: `http://localhost:8000`
API 문서: `http://localhost:8000/docs`

### 프론트엔드 실행

```bash
cd frontend
python -m http.server 8080
```

대시보드: `http://localhost:8080`

## 🛠️ 기술 스택

**백엔드:**
- FastAPI - Python 웹 프레임워크
- PostgreSQL - 데이터베이스
- SQLAlchemy - ORM
- WebSocket - 실시간 통신

**프론트엔드:**
- HTML5/CSS3/JavaScript
- Chart.js - 데이터 시각화
- WebSocket API - 실시간 알림

## 📡 API 엔드포인트

### 센서 데이터
- `POST /api/status` - 센서 데이터 저장
- `GET /api/status` - 최신 센서 데이터 조회
- `GET /api/sensor_log` - 센서 데이터 히스토리

### 화재 감지
- `POST /api/fire_alert` - 화재 알림 (3개 조건)
- `POST /api/manual_alert` - 수동 투하 알림 (2개 조건)
- `POST /api/drop` - 투하 명령
- `GET /api/fire_log` - 화재 경보 로그

### WebSocket
- `ws://localhost:8000/ws` - 실시간 알림

## ⚙️ 환경 설정

백엔드 폴더에 `.env` 파일 생성:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=firedrone
API_KEY=your-secret-api-key
```

## 🗄️ 데이터베이스

PostgreSQL 데이터베이스 생성:

```sql
CREATE DATABASE firedrone;
```

테이블은 서버 시작 시 자동 생성됩니다.

## 📝 개발 가이드

자세한 내용은 각 폴더의 README를 참조하세요:
- [백엔드 README](backend/README.md)
- 프론트엔드 README (TBD)

## 🤝 기여

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

