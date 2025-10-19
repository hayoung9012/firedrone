// ========== 차트 관련 ==========
let chart;
let sensorDataHistory = [];

/**
 * 차트 초기화
 */
function initChart() {
    const ctx = document.getElementById('sensorChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: '가스 (ppm)',
                    data: [],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1,
                    yAxisID: 'y'
                },
                {
                    label: '온도 (°C)',
                    data: [],
                    borderColor: 'rgb(255, 159, 64)',
                    tension: 0.1,
                    yAxisID: 'y1'
                },
                {
                    label: '고도 (m)',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: '가스 (ppm)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: '온도/고도'
                    },
                    grid: {
                        drawOnChartArea: false,
                    }
                }
            }
        }
    });
}

/**
 * 차트 데이터 업데이트
 * @param {Object} data - 센서 데이터 {gas, temp, altitude}
 */
function updateChartData(data) {
    // 히스토리 추가 (최대 30개)
    sensorDataHistory.push(data);
    if (sensorDataHistory.length > 30) {
        sensorDataHistory.shift();
    }
    
    // 차트 업데이트
    chart.data.labels = sensorDataHistory.map((_, i) => `${i * 3}초`);
    chart.data.datasets[0].data = sensorDataHistory.map(d => d.gas);
    chart.data.datasets[1].data = sensorDataHistory.map(d => d.temp);
    chart.data.datasets[2].data = sensorDataHistory.map(d => d.altitude);
    chart.update('none'); // 애니메이션 없이 업데이트
}

