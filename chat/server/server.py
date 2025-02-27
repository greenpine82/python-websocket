import asyncio
import websockets

CONNECTIONS = set()
PORT = 3000
async def handle(websocket):
  print('WS connection arrived')

  if websocket not in CONNECTIONS:
    CONNECTIONS.add(websocket)

  await websocket.send('Welcome to the chat!')

  closed = asyncio.ensure_future(websocket.wait_closed())
  closed.add_done_callback(lambda task: print('Connection closed'))

  async for message in websocket:
    websockets.broadcast(CONNECTIONS,message)

async def main():
  async with websockets.serve(handle, "localhost", PORT):
    print(f'Server running on port {PORT}')
    await asyncio.Future()  # run forever

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print('Server stopped')