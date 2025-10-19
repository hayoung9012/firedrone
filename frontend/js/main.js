// ========== 메인 로직 ==========

/**
 * 페이지 네비게이션 초기화
 */
function initNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = link.dataset.page;
            
            // 모든 페이지 숨기기
            document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            
            // 선택한 페이지 표시
            document.getElementById(pageName).classList.add('active');
            link.classList.add('active');
        });
    });
}

/**
 * 대시보드 업데이트
 * @param {Object} data - 센서 데이터 {ts, gas, temp, altitude}
 */
function updateDashboard(data) {
    // 센서 카드 업데이트
    document.getElementById('gasValue').textContent = Math.round(data.gas);
    document.getElementById('temp').textContent = data.temp.toFixed(1);
    document.getElementById('altitude').textContent = data.altitude.toFixed(1);
    document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString('ko-KR');
    
    // 차트 업데이트 (chart.js의 함수 호출)
    updateChartData(data);
}

/**
 * 센서값 로그 조회
 */
function initSensorLogButton() {
    document.getElementById('fetchSensorLogBtn').addEventListener('click', async () => {
        try {
            // 실제 API 호출
            const response = await fetch('http://localhost:8000/api/sensor_log?limit=50');
            const data = await response.json();
            
            const tbody = document.getElementById('sensorLogTableBody');
            tbody.innerHTML = data.map(row => `
                <tr>
                    <td>${new Date(row.ts).toLocaleString('ko-KR')}</td>
                    <td>${Math.round(row.gas)}</td>
                    <td>${row.temp.toFixed(1)}</td>
                    <td>${row.altitude.toFixed(1)}</td>
                </tr>
            `).join('');
        } catch (error) {
            alert('센서값 로그 조회 실패');
        }
    });
}

/**
 * 화재 경보 로그 조회
 */
function initFireLogButton() {
    document.getElementById('fetchFireLogBtn').addEventListener('click', async () => {
        try {
            // 실제 API 호출
            const response = await fetch('http://localhost:8000/api/fire_log');
            const fireAlertLog = await response.json();
            
            const tbody = document.getElementById('fireLogTableBody');
            if (fireAlertLog.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #999;">화재 경보 기록이 없습니다</td></tr>';
            } else {
                tbody.innerHTML = fireAlertLog.map(row => `
                    <tr style="background: ${row.conditions.includes('3개') ? '#ffebee' : '#fff3e0'};">
                        <td>${new Date(row.ts).toLocaleString('ko-KR')}</td>
                        <td><strong>${row.conditions}</strong></td>
                        <td>${Math.round(row.gas)} ppm</td>
                        <td>${row.ir.toFixed(1)} °C</td>
                        <td>${row.yolo ? '✅ 감지' : '❌ 미감지'}</td>
                        <td><span style="padding: 4px 12px; background: ${row.action.includes('자동') ? '#e74c3c' : '#f39c12'}; color: white; border-radius: 4px; font-size: 12px;">${row.action}</span></td>
                    </tr>
                `).join('');
            }
        } catch (error) {
            alert('화재 경보 로그 조회 실패');
        }
    });
}

/**
 * 초기화 및 시작
 */
window.addEventListener('load', () => {
    // 각 모듈 초기화
    initNavigation();
    initChart();
    initCameraControls();
    initSensorLogButton();
    initFireLogButton();
    connectWebSocket();
    
    // 3초마다 센서 데이터 폴링
    fetchSensorData();
    setInterval(fetchSensorData, 3000);
    
    // ========== 테스트용: 알림 시뮬레이션 (개발용) ==========
    // 30초 후 화재 알림 테스트
    setTimeout(() => {
        showFireAlert('🔥 화재 발생 감지! 가스: 520ppm, IR: 85°C, YOLO: 감지됨', {
            conditions: '3개 조건 충족',
            gas: 520,
            ir: 85,
            yolo: true,
            action: '자동 투하'
        });
    }, 30000);

    // 45초 후 수동 투하 알림 테스트
    setTimeout(() => {
        showManualDrop('🔥 2개 조건 충족 (가스 + IR) — 수동 투하하시겠습니까?');
    }, 45000);
});

