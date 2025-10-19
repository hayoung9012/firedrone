# 🚁 FireDrone Frontend

화재 진압 드론 모니터링 대시보드 프론트엔드

## 📋 프로젝트 소개

실시간으로 드론의 센서 데이터를 모니터링하고, 화재 감지 시 알림을 표시하는 웹 대시보드입니다.

### 주요 기능

- **실시간 센서 모니터링**
  - MQ-2 가스 센서 (ppm)
  - IR 온도 센서 (°C)
  - LiDAR 고도 센서 (m)

- **실시간 카메라 스트리밍**
  - 720p / 1080p 해상도 지원
  - 브라우저 카메라 접근

- **데이터 시각화**
  - Chart.js 기반 실시간 차트
  - 센서 데이터 추이 표시

- **화재 경보 시스템**
  - 3개 조건 충족 시 자동 투하
  - 2개 조건 충족 시 수동 투하 알림
  - 화재 경보 로그 기록

- **로그 조회**
  - 센서값 로그 (최근 50건)
  - 화재 경보 로그

## 📁 프로젝트 구조

```
firedrone-frontend/
├── index.html          # 메인 HTML 파일
├── css/
│   └── styles.css      # 전체 스타일시트
├── js/
│   ├── main.js         # 메인 로직 및 초기화
│   ├── websocket.js    # WebSocket 연결 및 데이터 폴링
│   ├── chart.js        # 차트 초기화 및 업데이트
│   └── camera.js       # 카메라 제어 및 모달
└── README.md           # 프로젝트 문서
```

## 🚀 실행 방법

### 1. 로컬에서 실행

간단한 HTTP 서버로 실행:

```bash
# Python 3
python -m http.server 8080

# Node.js (http-server 설치 필요)
npx http-server -p 8080

# VS Code Live Server 확장 사용
# index.html 우클릭 > "Open with Live Server"
```

브라우저에서 `http://localhost:8080` 접속

### 2. GitHub Pages 배포

1. GitHub 저장소 생성
2. 코드 푸시
3. Settings > Pages > Source를 `main` 브랜치로 설정
4. 배포된 URL로 접속

## 🔧 설정

### API 서버 연결

실제 백엔드 서버와 연결하려면 다음 파일을 수정하세요:

**js/websocket.js**
```javascript
// 라인 10: WebSocket 주소 변경
ws = new WebSocket('ws://your-server-address:port/ws');

// 라인 43: API 엔드포인트 주석 해제 및 수정
const response = await fetch('http://your-server-address:port/api/status');
```

## 🛠️ 사용 기술

- **HTML5** - 구조
- **CSS3** - 스타일링 (그라디언트, 애니메이션, 반응형)
- **JavaScript (Vanilla)** - 로직
- **Chart.js** - 데이터 시각화
- **WebSocket API** - 실시간 통신
- **Media Devices API** - 카메라 접근


## 🔗 백엔드 연동

이 프론트엔드는 다음 API 엔드포인트를 사용합니다:

- `ws://localhost:8000/ws` - WebSocket 실시간 연결
- `GET /api/status` - 현재 센서 상태
- `GET /api/sensor_log?limit=50` - 센서 로그 조회
- `GET /api/fire_log` - 화재 경보 로그 조회
- `POST /api/drop` - 수동 투하 명령

## 📝 개발 참고사항

### 테스트 모드

현재 더미 데이터로 동작합니다. 실제 서버 없이도 UI 테스트 가능:

- 센서 데이터: 3초마다 랜덤 생성
- 화재 알림: 30초 후 자동 표시
- 수동 투하 알림: 45초 후 자동 표시

### 프로덕션 배포 시

1. `js/main.js`에서 테스트용 setTimeout 제거 (라인 138~152)
2. `js/websocket.js`에서 더미 데이터 제거 및 실제 API 호출 활성화
3. 보안을 위해 HTTPS/WSS 사용 권장



