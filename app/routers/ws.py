import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.agents.flora_agent import make_runner

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()

    session = await make_runner().run()

    async with session:
        # Forward incoming audio/text from client to the agent session
        async def receive_from_client() -> None:
            try:
                while True:
                    message = await websocket.receive()
                    if "bytes" in message:
                        await session.send_audio(message["bytes"])
                    elif "text" in message:
                        data = json.loads(message["text"])
                        if data.get("type") == "message":
                            await session.send_message(data["content"])
            except WebSocketDisconnect:
                pass

        receive_task = asyncio.create_task(receive_from_client())

        try:
            async for event in session:
                if event.type == "audio":
                    await websocket.send_bytes(event.audio.data)
                elif event.type == "history_added":
                    await websocket.send_text(
                        json.dumps({"type": "history_added", "item": str(event.item)})
                    )
                elif event.type == "error":
                    await websocket.send_text(
                        json.dumps({"type": "error", "error": str(event.error)})
                    )
        except WebSocketDisconnect:
            pass
        finally:
            receive_task.cancel()
