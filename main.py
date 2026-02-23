import asyncio
import websockets
import json
import base64
import io
import os
import platform
import sys
from PIL import ImageGrab, Image
import pyautogui
import pydirectinput
import threading
import time

SERVER_URL = "wss://representatively-plastered-brain.ngrok-free.dev/socket.io/?EIO=4&transport=websocket"
DEVICE_ID = f"PC-{platform.node()}"
SCREEN_INTERVAL = 0.5
DOWNLOAD_DIR = os.path.expanduser("~/RMM_Downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def capture_screen():
    img = ImageGrab.grab()
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=70)
    return base64.b64encode(buffer.getvalue()).decode()

async def sender(ws):
    while True:
        try:
            frame = capture_screen()
            await ws.send('42["frame", {"id":"' + DEVICE_ID + '","frame":"' + frame + '"}]')
            await asyncio.sleep(SCREEN_INTERVAL)
        except Exception as e:
            print(f"Sender error: {e}")
            break

async def receiver(ws):
    while True:
        try:
            message = await ws.recv()
            if message.startswith('42['):
                _, payload = message.split('42', 1)
                data = json.loads(payload)
                typ = data[0]
                args = data[1]
                if typ == 'start_stream':
                    threading.Thread(target=asyncio.run, args=(sender(ws),), daemon=True).start()
                elif typ == 'input':
                    itype = args.get('type')
                    if itype == 'mouse':
                        action = args.get('action')
                        x = int(args.get('x'))
                        y = int(args.get('y'))
                        pyautogui.moveTo(x, y)
                        if action == 'down':
                            pydirectinput.mouseDown(button=args.get('button', 'left'))
                        elif action == 'up':
                            pydirectinput.mouseUp(button=args.get('button', 'left'))
                    elif itype == 'key':
                        pydirectinput.press(args.get('key'))
                elif typ == 'list_files':
                    files = os.listdir(DOWNLOAD_DIR)
                    await ws.send('42["file_list", {"files":' + json.dumps(files) + '}]')
                elif typ == 'upload_file':
                    name = args.get('name')
                    data = base64.b64decode(args.get('data'))
                    path = os.path.join(DOWNLOAD_DIR, name)
                    with open(path, 'wb') as f:
                        f.write(data)
        except Exception as e:
            print(f"Receiver error: {e}")
            break

async def client():
    while True:
        try:
            async with websockets.connect(SERVER_URL) as ws:
                print("Connected to server")
                # Register immediately after connection
                reg_msg = '42["register", {"id":"' + DEVICE_ID + '","type":"pc"}]'
                await ws.send(reg_msg)
                print(f"Sent registration for {DEVICE_ID}")
                await asyncio.gather(receiver(ws), asyncio.sleep(3600))
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 60s...")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print(f"Agent starting for {DEVICE_ID}")
    asyncio.run(client())

On Mon, Feb 23, 2026, 01:13 Silvas <silvasisback101@gmail.com> wrote:
import asyncio
import websockets
import json
import base64
import io
import os
import platform
import sys
from PIL import ImageGrab, Image
import pyautogui
import pydirectinput
import threading
import time

SERVER_URL = "wss://representatively-plastered-brain.ngrok-free.dev/socket.io/?EIO=4&transport=websocket"
DEVICE_ID = f"PC-{platform.node()}"
SCREEN_INTERVAL = 0.5
DOWNLOAD_DIR = os.path.expanduser("~/RMM_Downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def capture_screen():
    img = ImageGrab.grab()
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=70)
    return base64.b64encode(buffer.getvalue()).decode()

async def sender(ws):
    while True:
        try:
            frame = capture_screen()
            await ws.send('42["frame", {"id":"' + DEVICE_ID + '","frame":"' + frame + '"}]')
            await asyncio.sleep(SCREEN_INTERVAL)
        except Exception as e:
            print(f"Sender error: {e}")
            break

async def receiver(ws):
    while True:
        try:
            message = await ws.recv()
            if message.startswith('42['):
                _, payload = message.split('42', 1)
                data = json.loads(payload)
                typ = data[0]
                args = data[1]
                if typ == 'start_stream':
                    threading.Thread(target=asyncio.run, args=(sender(ws),), daemon=True).start()
                elif typ == 'input':
                    itype = args.get('type')
                    if itype == 'mouse':
                        action = args.get('action')
                        x = int(args.get('x'))
                        y = int(args.get('y'))
                        pyautogui.moveTo(x, y)
                        if action == 'down':
                            pydirectinput.mouseDown(button=args.get('button', 'left'))
                        elif action == 'up':
                            pydirectinput.mouseUp(button=args.get('button', 'left'))
                    elif itype == 'key':
                        pydirectinput.press(args.get('key'))
                elif typ == 'list_files':
                    files = os.listdir(DOWNLOAD_DIR)
                    await ws.send('42["file_list", {"files":' + json.dumps(files) + '}]')
                elif typ == 'upload_file':
                    name = args.get('name')
                    data = base64.b64decode(args.get('data'))
                    path = os.path.join(DOWNLOAD_DIR, name)
                    with open(path, 'wb') as f:
                        f.write(data)
        except Exception as e:
            print(f"Receiver error: {e}")
            break

async def client():
    while True:
        try:
            async with websockets.connect(SERVER_URL) as ws:
                print("Connected to server")
                # Register immediately after connection
                reg_msg = '42["register", {"id":"' + DEVICE_ID + '","type":"pc"}]'
                await ws.send(reg_msg)
                print(f"Sent registration for {DEVICE_ID}")
                await asyncio.gather(receiver(ws), asyncio.sleep(3600))
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 60s...")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print(f"Agent starting for {DEVICE_ID}")
    asyncio.run(client())

On Sun, Feb 22, 2026, 22:37 John Silvas <silvasjohn588@gmail.com> wrote:
import asyncio
import websockets
import json
import base64
import io
import os
import platform
import sys
from PIL import ImageGrab, Image
import pyautogui
import pydirectinput
import threading
import time

SERVER_URL = "wss://representatively-plastered-brain.ngrok-free.dev/socket.io/?EIO=4&transport=websocket"
DEVICE_ID = f"PC-{platform.node()}"
SCREEN_INTERVAL = 0.5
DOWNLOAD_DIR = os.path.expanduser("~/RMM_Downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def capture_screen():
    img = ImageGrab.grab()
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=70)
    return base64.b64encode(buffer.getvalue()).decode()

async def sender(ws):
    while True:
        try:
            frame = capture_screen()
            await ws.send('42["frame", {"id":"' + DEVICE_ID + '","frame":"' + frame + '"}]')
            await asyncio.sleep(SCREEN_INTERVAL)
        except Exception as e:
            print(f"Sender error: {e}")
            break

async def receiver(ws):
    while True:
        try:
            message = await ws.recv()
            if message.startswith('42['):
                _, payload = message.split('42', 1)
                data = json.loads(payload)
                typ = data[0]
                args = data[1]
                if typ == 'start_stream':
                    threading.Thread(target=asyncio.run, args=(sender(ws),), daemon=True).start()
                elif typ == 'input':
                    itype = args.get('type')
                    if itype == 'mouse':
                        action = args.get('action')
                        x = int(args.get('x'))
                        y = int(args.get('y'))
                        pyautogui.moveTo(x, y)
                        if action == 'down':
                            pydirectinput.mouseDown(button=args.get('button', 'left'))
                        elif action == 'up':
                            pydirectinput.mouseUp(button=args.get('button', 'left'))
                    elif itype == 'key':
                        pydirectinput.press(args.get('key'))
                elif typ == 'list_files':
                    files = os.listdir(DOWNLOAD_DIR)
                    await ws.send('42["file_list", {"files":' + json.dumps(files) + '}]')
                elif typ == 'upload_file':
                    name = args.get('name')
                    data = base64.b64decode(args.get('data'))
                    path = os.path.join(DOWNLOAD_DIR, name)
                    with open(path, 'wb') as f:
                        f.write(data)
        except Exception as e:
            print(f"Receiver error: {e}")
            break

async def client():
    while True:
        try:
            async with websockets.connect(SERVER_URL) as ws:
                await ws.send('42["register", {"id":"' + DEVICE_ID + '","type":"pc"}]')
                await asyncio.gather(receiver(ws), asyncio.sleep(3600))
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 60s...")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print(f"Agent starting for {DEVICE_ID}")
    asyncio.run(client())
