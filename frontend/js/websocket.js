// ========== WebSocket 및 데이터 폴링 ==========
let ws;

/**
 * WebSocket 연결
 */
function connectWebSocket() {
    // WebSocket 연결 (실제 서버 주소로 변경 필요)
    try {
        ws = new WebSocket('ws://localhost:8000/ws');
        
        ws.onopen = () => {
            console.log('WebSocket 연결됨');
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'fire_alert') {
                showFireAlert(data.message);
            } else if (data.type === 'manual_alert') {
                showManualDrop(data.message);
            }
        };
        
        ws.onerror = (error) => {
            console.log('WebSocket 연결 실패 (서버가 실행 중인지 확인하세요)');
        };
    } catch (error) {
        console.log('WebSocket 사용 불가 (데모 모드)');
    }
}

/**
 * 센서 데이터 폴링 (3초마다)
 */
async function fetchSensorData() {
    try {
        // 실제 API 호출
        const response = await fetch('http://localhost:8000/api/status');
        const data = await response.json();
        
        updateDashboard(data);
    } catch (error) {
        console.log('센서 데이터 조회 실패, 더미 데이터 사용');
        const data = {
            ts: new Date().toISOString(),
            gas: 300 + Math.random() * 100,
            temp: 22 + Math.random() * 5,
            altitude: 45 + Math.random() * 10
        };
        updateDashboard(data);
    }
}

