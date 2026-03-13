# F1 Dashboard

### Python Dependencies:
- uvicorn
- fastapi

### To run the server:

``` python
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

car_state = {
    "trc": 0.0,
    "air": 0.0,
    "hum": 0.0
}

@app.websocket("/ws")
async def f1_websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if "text" in payload:
                user_message = payload["text"]

                reponse = json.dumps(f"Message: '{user_message}'. Current car state: trc={car_state['trc']}, air={car_state['air']}, hum={car_state['hum']}")
                await websocket.send_text(reponse)

            elif "trc" in payload:
                car_state["trc"] = payload["trc"]
                car_state["air"] = payload["air"]
                car_state["hum"] = payload["hum"]
                
    except WebSocketDisconnect:
        print("disconnected")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    uvicorn.run(__name__ + ":app", host="127.0.0.1", port=8000, reload=True)
```

