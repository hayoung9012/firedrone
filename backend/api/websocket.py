from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket 연결됨. 현재 연결 수: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"WebSocket 연결 해제. 현재 연결 수: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """모든 연결된 클라이언트에게 메시지 전송"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"메시지 전송 실패: {e}")
                disconnected.append(connection)
        
        # 연결이 끊긴 클라이언트 제거
        for conn in disconnected:
            self.disconnect(conn)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """특정 클라이언트에게 메시지 전송"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"개인 메시지 전송 실패: {e}")
            self.disconnect(websocket)


# 전역 ConnectionManager 인스턴스
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 엔드포인트 핸들러"""
    await manager.connect(websocket)
    
    try:
        while True:
            # 클라이언트로부터 메시지 수신 (연결 유지용)
            data = await websocket.receive_text()
            
            # ping-pong 응답
            if data == "ping":
                await manager.send_personal_message({"type": "pong"}, websocket)
            else:
                # 다른 메시지 처리
                try:
                    message = json.loads(data)
                    print(f"수신된 메시지: {message}")
                except json.JSONDecodeError:
                    print(f"잘못된 JSON 형식: {data}")
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket 에러: {e}")
        manager.disconnect(websocket)

