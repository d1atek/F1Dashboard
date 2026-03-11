# F1 Dashboard

### Python Dependencies:
- uvicorn
- fastapi

### To run the server:

``` python
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def race_websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            race_state = {
                "message": "Engineer is analyzing data...",
                "trc": 50 + random.randint(-5, 5),
                "air": 30 + random.randint(-3, 3),
                "hum": 60 + random.randint(-5, 5)

            }
            await websocket.send_text(json.dumps(race_state))
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    uvicorn.run(__name__ + ":app", host="127.0.0.1", port=8000, reload=True)
```

