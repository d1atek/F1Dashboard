# F1 Dashboard

### Python Dependencies:
- uvicorn
- fastapi
- nest-asyncio

to install with uv:

``` bash
uv add uvicorn fastapi nest-asyncio
```

### To run the server:

Download the f1_server.py file from the repository:

``` bash
curl -O https://raw.githubusercontent.com/d1atek/F1Dashboard/main/server/f1_server.py
```

### Usage:

Run in terminal:

``` bash
python f1_server.py
```

Use in python:

``` python
from f1_server import server, start_server

async def your_handler(msg):
    # do something with msg
    await server.send_message(msg)

server.register_msg_handler(your_handler) 
await start_server()
```
