-- Drone Monitoring System - PostgreSQL Schema
-- Encoding: UTF-8
-- Safe to run multiple times if you add IF NOT EXISTS guards manually when needed.

-- 1) Sensor data log
CREATE TABLE IF NOT EXISTS sensor_log (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    gas NUMERIC(10, 2) NOT NULL,           -- MQ-2 가스 센서 (ppm)
    temp NUMERIC(5, 2) NOT NULL,           -- IR 온도 센서 (°C)
    altitude NUMERIC(6, 2) NOT NULL,       -- LiDAR 고도 센서 (m)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 시간 기반 조회 인덱스
CREATE INDEX IF NOT EXISTS idx_sensor_log_ts ON sensor_log(ts DESC);

-- 2) Fire alert log
CREATE TABLE IF NOT EXISTS fire_log (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    conditions VARCHAR(100) NOT NULL,      -- 감지 조건 (예: "3개 조건 충족")
    gas NUMERIC(10, 2) NOT NULL,           -- 감지 당시 가스값
    ir NUMERIC(5, 2) NOT NULL,             -- 감지 당시 IR 온도
    yolo BOOLEAN NOT NULL,                 -- YOLO 화재 감지 여부
    action VARCHAR(50) NOT NULL,           -- "자동 투하", "수동 투하"
    latitude NUMERIC(9, 6),                -- 위도
    longitude NUMERIC(9, 6),               -- 경도
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 조회 성능 인덱스
CREATE INDEX IF NOT EXISTS idx_fire_log_ts ON fire_log(ts DESC);
CREATE INDEX IF NOT EXISTS idx_fire_log_action ON fire_log(action);

-- 3) Drop history
CREATE TABLE IF NOT EXISTS drop_history (
    id SERIAL PRIMARY KEY,
    fire_log_id INTEGER REFERENCES fire_log(id),
    drop_type VARCHAR(20) NOT NULL,        -- "auto" | "manual"
    status VARCHAR(20) NOT NULL,           -- "success" | "failed" | "pending"
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    altitude NUMERIC(6, 2),
    error_message TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_drop_history_fire_log_id ON drop_history(fire_log_id);
CREATE INDEX IF NOT EXISTS idx_drop_history_executed_at ON drop_history(executed_at DESC);

-- 4) Drone status (current)
CREATE TABLE IF NOT EXISTS drone_status (
    id SERIAL PRIMARY KEY,
    drone_id VARCHAR(50) NOT NULL UNIQUE,
    battery_level NUMERIC(5, 2),
    is_online BOOLEAN DEFAULT TRUE,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    altitude NUMERIC(6, 2),
    drop_count INTEGER DEFAULT 0,
    remaining_drops INTEGER DEFAULT 5,
    last_heartbeat TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_drone_status_drone_id ON drone_status(drone_id);

-- 5) Camera snapshots (optional)
CREATE TABLE IF NOT EXISTS camera_snapshots (
    id SERIAL PRIMARY KEY,
    fire_log_id INTEGER REFERENCES fire_log(id),
    image_path VARCHAR(255) NOT NULL,
    image_size INTEGER,
    yolo_detected BOOLEAN,
    yolo_confidence NUMERIC(5, 4),
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_camera_snapshots_fire_log_id ON camera_snapshots(fire_log_id);

-- Sample initialization (optional)
-- INSERT INTO drone_status (drone_id, battery_level, is_online, remaining_drops)
-- VALUES ('DRONE_001', 100.0, true, 5);

-- Useful queries (reference)
-- SELECT ts, gas, temp, altitude FROM sensor_log ORDER BY ts DESC LIMIT 50;
-- SELECT ts, conditions, gas, ir, yolo, action FROM fire_log ORDER BY ts DESC;
-- SELECT DATE_TRUNC('hour', ts) AS hour, AVG(gas) AS avg_gas, AVG(temp) AS avg_temp,
--        AVG(altitude) AS avg_altitude, COUNT(*) AS record_count
-- FROM sensor_log
-- WHERE ts >= NOW() - INTERVAL '24 hours'
-- GROUP BY DATE_TRUNC('hour', ts)
-- ORDER BY hour DESC;
