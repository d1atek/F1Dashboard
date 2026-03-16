import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import nest_asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class F1Server:
    """A small reusable component to hold car condition and send messages.

    Usage:
      from f1_server import server
      server.get_condition()
      server.get_tire_state()
      await server.send_change_tire()
      server.register_msg_handler(handler)
      await server.send_message("hello")  # will send over websocket if connected, otherwise returns the formatted string
    """

    def __init__(self):
        self.cond_state = {
            "trc": 0.0,
            "air": 0.0,
            "hum": 0.0,
        }
        self.tire_state = {
            "fl": 0.0,
            "fr": 0.0,
            "rl": 0.0,
            "rr": 0.0,
        }
        # when a websocket client connects, we'll keep a reference here
        self._websocket: WebSocket | None = None
        self.msg_handler = None

    def register_msg_handler(self, handler):
        """Register a message handler function that takes a single string argument.

        This is a simple way to allow external code to react to incoming messages from the websocket.
        """
        self.msg_handler = handler

    def get_msg_handler(self):
        """Return the currently registered message handler, or None if no handler is registered."""
        return self.msg_handler

    def get_condition(self):
        """Return a copy of the current condition state."""
        return dict(self.cond_state)

    def get_tire_state(self):
        """Return a copy of the current tire state."""
        return dict(self.tire_state)

    def update_condition(self, trc: float | None = None, air: float | None = None, hum: float | None = None):
        """Update the internal condition state with any provided values."""
        if trc is not None:
            self.cond_state["trc"] = trc
        if air is not None:
            self.cond_state["air"] = air
        if hum is not None:
            self.cond_state["hum"] = hum

    def update_tire_state(self, fl: float | None = None, fr: float | None = None, rl: float | None = None, rr: float | None = None):
        """Update the internal tire state with any provided values."""
        if fl is not None:
            self.tire_state["fl"] = fl
        if fr is not None:
            self.tire_state["fr"] = fr
        if rl is not None:
            self.tire_state["rl"] = rl
        if rr is not None:
            self.tire_state["rr"] = rr

    def set_websocket(self, websocket: WebSocket):
        """Register a connected websocket to enable server->client pushes."""
        self._websocket = websocket

    def clear_websocket(self):
        self._websocket = None

    async def send_payload(self, payload: str):
        """Send a payload to the connected websocket if present.

        If no websocket is connected this returns the formatted response string.
        When a websocket is connected, the function returns True on success."""
        if self._websocket is not None:
            try:
                await self._websocket.send_text(payload)
                return True
            except Exception:
                # don't propagate websocket send errors; clear the websocket and return the payload
                self.clear_websocket()
                return payload
        return payload

    async def send_message(self, user_message: str):
        """Send a message to the connected websocket"""
        payload = json.dumps({"msg": user_message})
        return await self.send_payload(payload)

    async def send_tyre_change(self):
        """Send a tyre change to the connected websocket"""
        payload = json.dumps({"tyres": True})
        return await self.send_payload(payload)

    async def send_all_data(self, msg: str = ""):
        await self.send_message(msg+f" Condition: {self.get_condition()} Tire State: {self.get_tire_state()}")

# module-level instance for easy importing from other files
server = F1Server()
server.register_msg_handler(server.send_all_data)  # default message handler 

@app.websocket("/ws")
async def f1_websocket(websocket: WebSocket):
    await websocket.accept()
    server.set_websocket(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if "text" in payload:
                user_message = payload["text"]
                if server.get_msg_handler():
                    if asyncio.iscoroutinefunction(server.get_msg_handler()):
                        await server.get_msg_handler()(user_message)
                    else:
                        server.get_msg_handler()(user_message)

            elif "trc" in payload:
                # update condition using the component API
                server.update_condition(trc=payload.get("trc"), air=payload.get("air"), hum=payload.get("hum"))
                server.update_tire_state(fl=payload.get("fl"), fr=payload.get("fr"), rl=payload.get("rl"), rr=payload.get("rr"))

    except WebSocketDisconnect:
        print("disconnected")
    except Exception as e:
        print(e)
    finally:
        server.clear_websocket()

async def start_server():
    nest_asyncio.apply()
    
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    serveur_uvicorn = uvicorn.Server(config)
    await serveur_uvicorn.serve()

if __name__ == "__main__":
    asyncio.run(start_server())