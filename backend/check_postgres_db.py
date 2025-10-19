#!/usr/bin/env python3
"""
PostgreSQL 데이터베이스 내용 확인 스크립트
"""
import psycopg2
from config import settings

def check_database():
    try:
        # PostgreSQL 연결
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        
        print("🔍 PostgreSQL 데이터베이스 내용 확인")
        print("=" * 50)
        
        # 센서 데이터 확인
        print("\n📊 센서 데이터 (최근 5개):")
        cursor.execute("""
            SELECT id, ts, gas, temp, altitude 
            FROM sensor_readings 
            ORDER BY ts DESC 
            LIMIT 5
        """)
        
        sensor_data = cursor.fetchall()
        if sensor_data:
            for row in sensor_data:
                print(f"ID: {row[0]}, 시간: {row[1]}, 가스: {row[2]}ppm, 온도: {row[3]}°C, 고도: {row[4]}m")
        else:
            print("센서 데이터가 없습니다.")
        
        # 화재 알림 데이터 확인
        print("\n🔥 화재 알림 데이터:")
        cursor.execute("""
            SELECT id, ts, conditions, gas, ir, yolo, action 
            FROM fire_alerts 
            ORDER BY ts DESC 
            LIMIT 5
        """)
        
        fire_data = cursor.fetchall()
        if fire_data:
            for row in fire_data:
                print(f"ID: {row[0]}, 시간: {row[1]}, 조건: {row[2]}, 가스: {row[3]}, IR: {row[4]}, YOLO: {row[5]}, 액션: {row[6]}")
        else:
            print("화재 알림 데이터가 없습니다.")
        
        # 전체 개수 확인
        cursor.execute("SELECT COUNT(*) FROM sensor_readings")
        sensor_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM fire_alerts")
        fire_count = cursor.fetchone()[0]
        
        print(f"\n📈 총 데이터 개수:")
        print(f"  - 센서 데이터: {sensor_count}개")
        print(f"  - 화재 알림: {fire_count}개")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    check_database()
