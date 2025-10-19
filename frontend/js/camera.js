// ========== 카메라 제어 및 모달 ==========
let videoStream;
let fireAlertLog = []; // 화재 경보 로그 저장

/**
 * 카메라 컨트롤 초기화
 */
function initCameraControls() {
    // 카메라 시작 버튼
    document.getElementById('startCameraBtn').addEventListener('click', async () => {
        const resolution = document.getElementById('resolutionSelect').value;
        const width = resolution === '720' ? 1280 : 1920;
        const height = resolution === '720' ? 720 : 1080;
        
        try {
            videoStream = await navigator.mediaDevices.getUserMedia({
                video: { width, height },
                audio: false
            });
            
            document.getElementById('videoElement').srcObject = videoStream;
            document.getElementById('startCameraBtn').style.display = 'none';
            document.getElementById('stopCameraBtn').style.display = 'inline-block';
            document.getElementById('resolutionSelect').disabled = true;
        } catch (error) {
            alert('카메라 접근 실패: ' + error.message);
        }
    });

    // 카메라 중지 버튼
    document.getElementById('stopCameraBtn').addEventListener('click', () => {
        if (videoStream) {
            videoStream.getTracks().forEach(track => track.stop());
            document.getElementById('videoElement').srcObject = null;
            document.getElementById('startCameraBtn').style.display = 'inline-block';
            document.getElementById('stopCameraBtn').style.display = 'none';
            document.getElementById('resolutionSelect').disabled = false;
        }
    });
}

/**
 * 화재 알림 모달 표시
 * @param {string} message - 알림 메시지
 * @param {Object} data - 화재 데이터 (조건, 가스값, IR, YOLO 등)
 */
function showFireAlert(message, data = null) {
    document.getElementById('fireAlertMessage').textContent = message;
    document.getElementById('fireAlertModal').classList.add('show');
    
    // 로그에 추가
    if (data) {
        fireAlertLog.unshift({
            ts: new Date().toISOString(),
            conditions: data.conditions || '3개 조건 충족',
            gas: data.gas || 0,
            ir: data.ir || 0,
            yolo: data.yolo || false,
            action: data.action || '자동 투하'
        });
    }
    
    // 소리 알림 (옵션)
    const audio = new Audio('data:audio/wav;base64,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');
    audio.play().catch(() => {});
}

/**
 * 화재 알림 모달 닫기
 */
function closeFireAlert() {
    document.getElementById('fireAlertModal').classList.remove('show');
}

/**
 * 수동 투하 모달 표시
 * @param {string} message - 알림 메시지
 */
function showManualDrop(message) {
    document.getElementById('manualDropMessage').textContent = message;
    document.getElementById('manualDropModal').classList.add('show');
}

/**
 * 수동 투하 모달 닫기
 */
function closeManualDrop() {
    document.getElementById('manualDropModal').classList.remove('show');
}

/**
 * 투하 확인
 */
async function confirmDrop() {
    try {
        // 실제 API 호출
        // await fetch('http://localhost:8000/api/drop', { method: 'POST' });
        
        alert('투하 명령이 전송되었습니다!');
        closeManualDrop();
    } catch (error) {
        alert('투하 명령 전송 실패');
    }
}

