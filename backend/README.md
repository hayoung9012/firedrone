# 🚁 Fire Drone Backend

드론 화재 감지 모니터링 시스템의 백엔드 API 서버입니다.

## 🛠️ 기술 스택

- **FastAPI** - 고성능 비동기 웹 프레임워크
- **PostgreSQL** - 센서 데이터 & 로그 저장
- **WebSocket** - 실시간 알림
- **SQLAlchemy** - ORM
- **Pydantic** - 데이터 검증

---

## 📦 설치 방법

### 1️⃣ Python 가상환경 생성 (권장)

```powershell
cd C:\firedrone-backend
python -m venv venv
```

### 2️⃣ 가상환경 활성화

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\venv\Scripts\activate.bat
```

### 3️⃣ 의존성 설치

```powershell
pip install -r requirements.txt
```

---

## 🗄️ PostgreSQL 설정

### 설치
1. PostgreSQL 다운로드: https://www.postgresql.org/download/
2. 설치 시 비밀번호 설정 (기억해두세요!)

### 데이터베이스 생성

```sql
-- psql 또는 pgAdmin에서 실행
CREATE DATABASE firedrone;
```

### 환경 변수 설정

`C:\firedrone-backend` 폴더에 `.env` 파일 생성:

```env
# PostgreSQL 설정
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=firedrone

# API 키 (보안)
API_KEY=my-secret-key-12345

# CORS (프론트엔드 주소)
CORS_ORIGINS=http://localhost:8080,http://192.168.0.100:8080
```

---

## 🚀 실행 방법

### 개발 모드 (자동 재시작)

```powershell
python main.py
```

또는

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면:
- API 문서: http://localhost:8000/docs
- WebSocket: ws://localhost:8000/ws

---

## 📡 API 엔드포인트

### 센서 데이터

| 메소드 | 경로 | 설명 | 인증 |
|--------|------|------|------|
| `POST` | `/api/status` | 센서 데이터 저장 (젯슨 → 서버) | API Key 필요 |
| `GET` | `/api/status` | 최신 센서 데이터 조회 | 불필요 |
| `GET` | `/api/sensor_log` | 센서 데이터 히스토리 | 불필요 |

### 화재 감지

| 메소드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/api/fire_alert` | 화재 알림 (3개 조건) |
| `POST` | `/api/manual_alert` | 수동 투하 알림 (2개 조건) |
| `POST` | `/api/drop` | 투하 명령 |
| `GET` | `/api/fire_log` | 화재 경보 로그 조회 |

### WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.type, data.message);
};
```

---

## 🔐 API 키 인증

센서 데이터 저장 시 API 키가 필요합니다:

```python
import requests

headers = {
    "X-API-KEY": "my-secret-key-12345"
}

data = {
    "gas": 350.5,
    "temp": 25.3,
    "altitude": 45.2
}

response = requests.post(
    "http://localhost:8000/api/status",
    json=data,
    headers=headers
)
```

---

## 📊 데이터베이스 스키마

### sensor_readings (센서 데이터)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | BIGINT | 자동 증가 ID |
| ts | TIMESTAMP | 측정 시각 |
| gas | FLOAT | 가스 센서 (ppm) |
| temp | FLOAT | 온도 (°C) |
| altitude | FLOAT | 고도 (m) |

### fire_alerts (화재 경보)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | BIGINT | 자동 증가 ID |
| ts | TIMESTAMP | 발생 시각 |
| conditions | STRING | 조건 ("3개 충족" 등) |
| gas | FLOAT | 가스값 |
| ir | FLOAT | IR 온도 |
| yolo | BOOLEAN | YOLO 감지 여부 |
| action | STRING | 조치 ("자동 투하" 등) |
| lat | FLOAT | 위도 (옵션) |
| lon | FLOAT | 경도 (옵션) |

---

## 🔧 개발 팁

### API 문서 자동 생성

FastAPI는 자동으로 API 문서를 생성합니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 데이터베이스 초기화

서버 첫 실행 시 자동으로 테이블이 생성됩니다.

수동으로 초기화하려면:

```python
from database import init_db
init_db()
```

### 로그 확인

서버 실행 시 콘솔에 로그가 출력됩니다:
- WebSocket 연결/해제
- API 요청
- 에러 메시지

---

## 🌐 외부 접속 설정

다른 기기(젯슨, 다른 노트북)에서 접속하려면:

1. **방화벽 열기** (Windows)
   - 포트 8000 허용

2. **IP 주소 확인**
   ```powershell
   ipconfig
   ```
   예: `192.168.0.100`

3. **접속 주소**
   - API: `http://192.168.0.100:8000`
   - WebSocket: `ws://192.168.0.100:8000/ws`

---

## 📝 TODO

- [ ] 젯슨 투하 명령 실제 구현
- [ ] 센서 데이터 이상치 검증
- [ ] 로그 파일 저장
- [ ] 사용자 인증 (JWT)
- [ ] HTTPS 설정

---

## 🐛 문제 해결

### PostgreSQL 연결 실패
```
⚠️ 데이터베이스 초기화 실패
```
- PostgreSQL 서비스가 실행 중인지 확인
- `.env` 파일의 비밀번호 확인

### CORS 에러
- `config.py`의 `CORS_ORIGINS`에 프론트엔드 주소 추가

### WebSocket 연결 안 됨
- 방화벽에서 8000 포트 허용
- 프론트엔드에서 `ws://` (https 아님) 사용

---

## 📞 연락처

문제가 있으면 이슈를 등록하세요!

